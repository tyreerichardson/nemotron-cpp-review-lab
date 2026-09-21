#include <vector>
bool contains(const std::vector<int>& values, int target) {
    for (const auto value : values)
        if (value == target) return true;
    return false;
}
