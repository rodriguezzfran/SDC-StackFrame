#!/bin/bash

# Crear la carpeta build
mkdir -p build

# Compilar el código de ensamblador con información de depuración
nasm -f elf64 -g -F dwarf -o build/add_one.o src/Calculator_ASM.asm

# Compilar el código C con información de depuración
gcc -g -c -fPIC -o build/libcalc.o src/calculator.c

# Enlazar los archivos objeto para crear la biblioteca compartida
gcc -shared -o build/libcalc.so build/libcalc.o build/add_one.o
