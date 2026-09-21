int first_value() {
    int* values = new int[3]{4, 8, 15};
    int result = values[0];
    delete values;
    return result;
}
