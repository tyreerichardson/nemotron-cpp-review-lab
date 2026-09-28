const example = {
  file: "out_of_bounds.cpp",
  source: `#include <vector>
int sum(const std::vector<int>& values) {
    int total = 0;
    for (std::size_t i = 0; i <= values.size(); ++i)
        total += values[i];
    return total;
}`,
};

const filename = document.getElementById("filename");
const source = document.getElementById("source");
const lineNumbers = document.getElementById("line-numbers");
const sourceMeta = document.getElementById("source-meta");
const status = document.querySelector(".status");
const statusText = document.getElementById("status-text");
const resultState = document.getElementById("result-state");
const resultOutput = document.getElementById("review-output");
const emptyState = document.getElementById("empty-state");
const errorOutput = document.getElementById("error-output");
const reviewButton = document.getElementById("review-button");
const reviewButtonText = document.getElementById("review-button-text");
let latestReview = null;

function renderLineNumbers(activeLine = 0) {
  const count = source.value.split("\n").length;
  lineNumbers.replaceChildren();
  for (let line = 1; line <= count; line += 1) {
    const marker = document.createElement("span");
    marker.textContent = line;
    marker.classList.toggle("active", line === activeLine);
    lineNumbers.append(marker);
  }
  const bytes = new TextEncoder().encode(source.value).length;
  sourceMeta.textContent = `${count} ${count === 1 ? "line" : "lines"} · ${bytes} bytes`;
}

function setResultState(value, text) {
  resultState.dataset.state = value;
  resultState.textContent = text;
}

function makeBadge(text, type = "") {
  const badge = document.createElement("span");
  badge.className = `badge ${type}`;
  badge.textContent = text;
  return badge;
}

function renderReview(review, elapsed, recorded = false) {
  latestReview = review;
  emptyState.hidden = true;
  errorOutput.hidden = true;
  resultOutput.hidden = false;
  document.getElementById("summary").textContent = review.summary || "No summary supplied";
  const list = document.getElementById("finding-list");
  list.replaceChildren();
  let activeLine = 0;
  if (review.findings.length === 0) {
    const clean = document.createElement("div");
    clean.className = "finding clean";
    clean.textContent = "No supported findings in this review.";
    list.append(clean);
  }
  for (const finding of review.findings) {
    activeLine = finding.location.start_line;
    const card = document.createElement("article");
    card.className = "finding";
    const top = document.createElement("div");
    top.className = "finding-top";
    top.append(
      makeBadge(finding.category),
      makeBadge(finding.severity, "severity"),
      makeBadge(`line ${finding.location.start_line}`, "line"),
    );
    const title = document.createElement("h3");
    title.textContent = finding.title;
    const explanation = document.createElement("p");
    explanation.textContent = finding.explanation;
    const fix = document.createElement("p");
    fix.className = "fix";
    fix.textContent = `Suggested fix: ${finding.suggested_fix}`;
    card.append(top, title, explanation, fix);
    list.append(card);
  }
  renderLineNumbers(activeLine);
  document.getElementById("result-meta").textContent = recorded
    ? `Recorded, schema-validated review · 2026-09-21 · ${review.file}`
    : `Schema validated · ${elapsed.toFixed(1)}s · ${review.file}`;
  document.getElementById("raw-json").textContent = JSON.stringify(review, null, 2);
  setResultState(recorded ? "recorded" : "valid", recorded ? "Saved example" : "Live result");
}

function showError(message) {
  latestReview = null;
  emptyState.hidden = true;
  resultOutput.hidden = true;
  errorOutput.hidden = false;
  errorOutput.textContent = message;
  setResultState("error", "Review failed");
}

function resetResult() {
  latestReview = null;
  emptyState.hidden = false;
  resultOutput.hidden = true;
  errorOutput.hidden = true;
  setResultState("", "Ready");
}

async function checkHealth() {
  try {
    const response = await fetch("/api/health", { cache: "no-store" });
    const data = await response.json();
    status.dataset.state = data.available ? "online" : "offline";
    statusText.textContent = data.available ? "Model connected" : "Model unavailable";
    document.getElementById("endpoint-label").textContent = data.endpoint;
  } catch {
    status.dataset.state = "offline";
    statusText.textContent = "Connection unavailable";
  }
}

async function runReview() {
  reviewButton.disabled = true;
  filename.disabled = true;
  source.disabled = true;
  document.getElementById("load-example").disabled = true;
  document.getElementById("saved-example").disabled = true;
  reviewButtonText.textContent = "Reviewing…";
  setResultState("", "Reviewing…");
  errorOutput.hidden = true;
  try {
    const response = await fetch("/api/review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ file: filename.value.trim(), source: source.value }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
    renderReview(data.review, data.elapsed_seconds);
    checkHealth();
  } catch (error) {
    showError(error.message);
  } finally {
    reviewButton.disabled = false;
    filename.disabled = false;
    source.disabled = false;
    document.getElementById("load-example").disabled = false;
    document.getElementById("saved-example").disabled = false;
    reviewButtonText.textContent = "Review code";
  }
}

source.addEventListener("input", () => { renderLineNumbers(); resetResult(); });
filename.addEventListener("input", resetResult);
source.addEventListener("scroll", () => { lineNumbers.scrollTop = source.scrollTop; });
source.addEventListener("keydown", (event) => {
  if (event.key !== "Tab") return;
  event.preventDefault();
  const start = source.selectionStart;
  source.setRangeText("    ", start, source.selectionEnd, "end");
  renderLineNumbers();
  resetResult();
});
document.getElementById("load-example").addEventListener("click", () => {
  filename.value = example.file;
  source.value = example.source;
  renderLineNumbers();
  resetResult();
});
reviewButton.addEventListener("click", runReview);
document.getElementById("saved-example").addEventListener("click", async () => {
  filename.value = example.file;
  source.value = example.source;
  try {
    const response = await fetch("/demo.json", { cache: "no-store" });
    if (!response.ok) throw new Error("Could not load the saved example");
    renderReview(await response.json(), 0, true);
  } catch (error) {
    showError(error.message);
  }
});
document.getElementById("copy-json").addEventListener("click", async () => {
  if (!latestReview) return;
  await navigator.clipboard.writeText(JSON.stringify(latestReview, null, 2));
  const button = document.getElementById("copy-json");
  button.textContent = "Copied";
  setTimeout(() => { button.textContent = "Copy JSON"; }, 1800);
});
renderLineNumbers();
checkHealth();
setInterval(checkHealth, 15000);
