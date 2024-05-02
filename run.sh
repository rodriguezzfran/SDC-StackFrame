#!/bin/bash

# Comprobar si la carpeta build existe
if [ -d "build" ]; then
    # Si existe, ejecutar el programa en Python
    python3 src/GINI_interface.py
else
    # Si no existe, imprimir un mensaje de error
    echo "Error: la carpeta build no existe. Por favor, ejecuta el script de build primero."
fi
