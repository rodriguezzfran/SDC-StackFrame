cmake_minimum_required(VERSION 3.10)
project(calculator C)
add_library(calc SHARED calculator.c)
set_target_properties(calc PROPERTIES VERSION 1.0 SOVERSION 1)

# Asegúrate de que Python está instalado
find_package(Python3 COMPONENTS Interpreter REQUIRED)

# Agrega un comando personalizado para ejecutar el script Python
add_custom_command(TARGET calc POST_BUILD COMMAND Python3::Interpreter ${CMAKE_SOURCE_DIR}/GINI_interface.py)