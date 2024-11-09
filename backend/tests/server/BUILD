py_test(
    name = "test_extract_items",
    srcs = ["test_extract_items.py"],
    deps = [
        "//src/server:extract_items", 
        "//src/data_models:receipt",
        "//src/data_models:item",
    ],
)


py_test(
    name = "test_store_items",
    srcs = ["test_store_items.py"],
    deps = ["//src/server:store_items", "//src/data_models:item"],
)