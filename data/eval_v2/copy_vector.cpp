#include <vector>
long total(const std::vector<int>& values) {
    long result = 0;
    const auto values_copy = values;
    for (const int value : values_copy)
        result += value;
    return result;
}
