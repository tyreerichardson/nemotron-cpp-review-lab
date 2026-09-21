#include <array>
int days_in_month(int month) {
    constexpr std::array<int, 12> days{31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    return days[month];
}
