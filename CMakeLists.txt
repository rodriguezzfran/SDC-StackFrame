cmake_minimum_required(VERSION 3.10)
project(calculator C)
add_library(calc SHARED calculator.c)
set_target_properties(calc PROPERTIES VERSION 1.0 SOVERSION 1)

# Agrega un comando personalizado para ejecutar el script Python
add_custom_command(TARGET calc POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_BINARY_DIR}/libcalc.so ${CMAKE_SOURCE_DIR})
