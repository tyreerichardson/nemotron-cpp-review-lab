#include <string>
#include <vector>
bool has_duplicate(const std::vector<std::string>& words) {
    for (std::size_t i = 0; i < words.size(); ++i)
        for (std::size_t j = i + 1; j < words.size(); ++j)
            if (words[i] == words[j]) return true;
    return false;
}
