#include <algorithm>
#include <vector>
void cap_all(std::vector<int>& values) {
    std::transform(values.begin(), values.end(), values.begin(), [](int value) {
        return std::clamp(value, 0, 100);
    });
}
