#!/bin/bash

# Borrar la carpeta build si existe
if [ -d "build" ]; then
    rm -r build
fi

# Crear la carpeta build
mkdir build

# Compilar el código de ensamblador
nasm -f elf64 -o build/add_one.o src/Calculator_ASM.asm

# Compilar el código C
gcc -c -fPIC -o build/libcalc.o src/calculator.c

# Enlazar los archivos objeto para crear la biblioteca compartida
gcc -shared -o build/libcalc.so build/libcalc.o build/add_one.o
