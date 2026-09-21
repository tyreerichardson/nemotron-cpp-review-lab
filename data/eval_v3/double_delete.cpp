void destroy_twice() {
    int* value = new int(7);
    delete value;
    delete value;
}
