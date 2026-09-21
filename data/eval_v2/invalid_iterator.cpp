#include <vector>
int read_after_growth() {
    std::vector<int> values{1, 2};
    auto first = values.begin();
    values.push_back(3);
    return *first;
}
