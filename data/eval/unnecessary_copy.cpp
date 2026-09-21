#include <string>
#include <vector>
std::size_t total_length(const std::vector<std::string>& words) {
    std::size_t total = 0;
    for (auto word : words)
        total += word.size();
    return total;
}
