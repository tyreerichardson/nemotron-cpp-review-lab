#include <string>
#include <vector>
std::string join(const std::vector<std::string>& parts) {
    std::string result;
    for (const auto& part : parts) result += part;
    return result;
}
