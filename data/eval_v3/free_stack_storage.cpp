#include <cstdlib>
void release_buffer() {
    char buffer[16]{};
    std::free(buffer);
}
