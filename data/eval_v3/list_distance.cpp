#include <iterator>
#include <list>
#include <cstddef>
std::size_t position_sum(const std::list<int>& values) {
    std::size_t sum = 0;
    for (auto it = values.begin(); it != values.end(); ++it)
        sum += std::distance(values.begin(), it);
    return sum;
}
