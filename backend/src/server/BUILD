load("@rules_python//python:defs.bzl", "py_binary")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "extract_items",
    srcs = ["extract_items.py"],
    deps = ["//src/data_models:receipt"]
)

py_library(
    name = "store_items",
    srcs = ["store_items.py"],
    deps = ["//src/data_models:item"]
)