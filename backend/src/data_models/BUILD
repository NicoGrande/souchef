load("@rules_python//python:defs.bzl", "py_library")

package(default_visibility = ["//visibility:public"])


py_library(
    name = "item",
    srcs = ["item.py"],
    deps = [":quantity", "//backend/src/utils:types"]
)

py_library(
    name = "quantity",
    srcs = ["quantity.py"],
    deps = ["//backend/src/utils:types"]
)

py_library(
    name = "recipe",
    srcs = ["recipe.py"],
    deps = [":item", ":quantity", "//backend/src/utils:types"]
)