#include <vector>
int max_or(const std::vector<int>& values, int fallback) {
    int result = fallback;
    for (const int value : values)
        if (value > result) result = value;
    return result;
}
