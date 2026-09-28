#!/usr/bin/env python3
"""Local visual front end for the existing schema-validated C++ reviewer."""

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import time
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen

import cli


ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"
SCHEMA = json.loads((ROOT / "schemas/review.schema.json").read_text())
ASSETS = {
    "/": (WEB / "index.html", "text/html; charset=utf-8"),
    "/app.js": (WEB / "app.js", "text/javascript; charset=utf-8"),
    "/styles.css": (WEB / "styles.css", "text/css; charset=utf-8"),
    "/demo.json": (WEB / "demo.json", "application/json; charset=utf-8"),
}
FILE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,100}\.cpp\Z")


def models_url(endpoint):
    parts = urlsplit(endpoint)
    return urlunsplit((parts.scheme, parts.netloc, "/v1/models", "", ""))


def make_handler(endpoint, model, timeout):
    class Handler(BaseHTTPRequestHandler):
        server_version = "NemotronVisual/1.0"

        def _headers(self, status, content_type, length):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(length))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'")
            self.end_headers()

        def _json(self, status, value):
            body = json.dumps(value).encode("utf-8")
            self._headers(status, "application/json; charset=utf-8", len(body))
            self.wfile.write(body)

        def _same_origin(self):
            origin = self.headers.get("Origin")
            host = self.headers.get("Host", "")
            allowed_hosts = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
            return host in allowed_hosts and (not origin or origin == "http://" + host)

        def do_GET(self):
            if self.path == "/api/health":
                try:
                    with urlopen(Request(models_url(endpoint)), timeout=2) as response:
                        available = response.status == 200
                except (OSError, ValueError):
                    available = False
                self._json(200, {"available": available, "endpoint": endpoint, "model": model})
                return
            asset = ASSETS.get(self.path)
            if not asset:
                self._json(404, {"error": "not found"})
                return
            content = asset[0].read_bytes()
            self._headers(200, asset[1], len(content))
            self.wfile.write(content)

        def do_POST(self):
            if self.path != "/api/review":
                self._json(404, {"error": "not found"})
                return
            if not self._same_origin() or self.headers.get("Content-Type", "").split(";", 1)[0] != "application/json":
                self._json(403, {"error": "request must come from this local page"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= cli.LIMIT + 4096:
                    raise ValueError("request exceeds the size limit")
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                if not isinstance(payload, dict) or set(payload) != {"file", "source"}:
                    raise ValueError("request must contain file and source")
                name, source = payload["file"], payload["source"]
                if not isinstance(name, str) or not FILE_NAME.fullmatch(name):
                    raise ValueError("use a simple .cpp file name")
                if not isinstance(source, str) or not source.strip() or len(source.encode("utf-8")) > cli.LIMIT:
                    raise ValueError("source must be nonempty UTF-8 text under 32 KiB")
                start = time.monotonic()
                content, _ = cli.infer(endpoint, model, SCHEMA, cli.prompt_for(name, source), timeout, 0)
                review = json.loads(cli.normalize_content(content))
                cli.validate(review, name, len(source.splitlines()))
                self._json(200, {"review": review, "elapsed_seconds": round(time.monotonic() - start, 1)})
            except (OSError, RuntimeError, TypeError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
                self._json(400, {"error": str(exc)})

        def log_message(self, format_string, *args):
            print("visual_app: " + format_string % args)

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--endpoint", default=cli.DEFAULT_ENDPOINT)
    parser.add_argument("--model", default=cli.DEFAULT_MODEL)
    parser.add_argument("--timeout", type=float, default=90)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535 or args.timeout <= 0:
        parser.error("port and timeout must be positive")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(args.endpoint, args.model, args.timeout))
    print(f"Visual reviewer: http://127.0.0.1:{args.port}", flush=True)
    print(f"Model endpoint: {args.endpoint}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
