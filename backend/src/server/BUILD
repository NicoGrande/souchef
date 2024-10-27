load("@rules_python//python:defs.bzl", "py_binary")

package(default_visibility = ["//visibility:public"])

py_binary(
    name = "extract_items",
    srcs = ["extract_items.py"],
    deps = ["//backend/src/data_models:receipt"]
)
