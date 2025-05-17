cmake_minimum_required(VERSION 3.15)
project(LANGUAGES CXX)

add_library(MemoryManagementC SHARED MemoryFunctions.cpp)
target_compile_definitions(MemoryManagementC PRIVATE _WINDLL)