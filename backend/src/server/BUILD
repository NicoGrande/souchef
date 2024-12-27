load("@rules_python//python:defs.bzl", "py_binary")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "extract_items",
    srcs = ["extract_items.py"],
    deps = [
        "//src/data_models:receipt",
        "@pip//pydantic",
        "@pip//langchain",
        "@pip//validators",
        "@pip//langchain_google_community",
        "@pip//langchain_openai",
        "@pip//firebase_admin"
    ]
)

py_library(
    name = "store_items",
    srcs = ["store_items.py"],
    deps = [
        "//src/data_models:item", 
        "@pip//pydantic", 
        "@pip//langchain", 
        "@pip//langchain_google_community", 
        "@pip//langchain_openai",
        "@pip//firebase_admin"
    ]
)

py_binary(
    name = "create_recipe",
    srcs = ["create_recipe.py"],
    deps = [
        "//src/data_models:recipe",
        "//src/data_models:item",
        "//src/data_models:quantity",
        "//src/utils:types",
        "@pip//pydantic",
        "@pip//langchain",
        "@pip//langchain_google_community",
        "@pip//langchain_openai"
    ]
)