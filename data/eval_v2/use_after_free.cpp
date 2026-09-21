int first_after_delete() {
    int* values = new int[2]{4, 9};
    int* saved = values;
    delete[] values;
    return saved[0];
}
