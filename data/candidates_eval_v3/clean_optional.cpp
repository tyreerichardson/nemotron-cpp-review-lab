#include <optional>
int value_or(const std::optional<int>& value, int fallback) {
    if (value) return *value;
    return fallback;
}
