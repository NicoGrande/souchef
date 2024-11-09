load("@rules_python//python:defs.bzl", "py_library")

package(default_visibility = ["//visibility:public"])


py_library(
    name = "item",
    srcs = ["item.py"],
    deps = [":quantity", "//src/utils:types"]
)

py_library(
    name = "quantity",
    srcs = ["quantity.py"],
    deps = ["//src/utils:types"]
)

py_library(
    name = "recipe",
    srcs = ["recipe.py"],
    deps = [":item", ":quantity", "//src/utils:types"]
)

py_library(
    name = "receipt",
    srcs = ["receipt.py"],
    deps = [":item", "//src/utils:types"]
)
