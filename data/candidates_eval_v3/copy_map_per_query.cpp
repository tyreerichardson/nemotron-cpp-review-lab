#include <map>
#include <string>
#include <vector>
int count_known(const std::map<std::string, int>& scores, const std::vector<std::string>& names) {
    int count = 0;
    for (const auto& name : names) {
        auto snapshot = scores;
        if (snapshot.find(name) != snapshot.end()) ++count;
    }
    return count;
}
