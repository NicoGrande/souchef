load("@rules_python//python:defs.bzl", "py_test")


py_test(
    name = "test_item",
    srcs = ["test_item.py"],
    deps = [
        "//src/data_models:item", 
        "//src/data_models:quantity", 
        "//src/utils:types",
        "@pip//pytest"
    ]
)


py_test(
    name = "test_quantity",
    srcs = ["test_quantity.py"],
    deps = [
        "//src/data_models:quantity", 
        "//src/utils:types",
        "@pip//pytest"
    ]
)


py_test(
    name = "test_recipe",
    srcs = ["test_recipe.py"],
    deps = [
        "//src/data_models:recipe", 
        "//src/utils:types",
        "@pip//pytest"
    ]
)

py_test(
    name = "test_receipt",
    srcs = ["test_receipt.py"],
    deps = [
        "//src/data_models:receipt", 
        "//src/utils:types",
        "@pip//pytest"
    ]
)
