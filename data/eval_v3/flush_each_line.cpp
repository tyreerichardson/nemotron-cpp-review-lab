#include <ostream>
#include <vector>
void write_lines(std::ostream& out, const std::vector<int>& values) {
    for (int value : values) {
        out << value << '\n';
        out.flush();
    }
}
