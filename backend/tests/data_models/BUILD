load("@rules_python//python:defs.bzl", "py_test")


py_test(
    name = "test_item",
    srcs = ["test_item.py"],
    deps = [
        "//backend/src/data_models:item", 
        "//backend/src/data_models:quantity", 
        "//backend/src/utils:types"
    ]
)


py_test(
    name = "test_quantity",
    srcs = ["test_quantity.py"],
    deps = [
        "//backend/src/data_models:quantity", 
        "//backend/src/utils:types"
    ]
)


py_test(
    name = "test_recipe",
    srcs = ["test_recipe.py"],
    deps = [
        "//backend/src/data_models:recipe", 
        "//backend/src/utils:types"
    ]
)