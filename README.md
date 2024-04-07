# SDC-StackFrame

### Uso para compilar y correr el programa

En la carpeta raíz del repositorio ejecutar los siguientes comandos:

```bash
mkdir build
cd build
cmake ..
make
cd ..
python3 GINI_interface.py
```

# SdC 2024 - Trabajo Práctico N° 2

## Introducción

El objetivo del siguiente trabajo es diseñar e implementar una interfaz que muestre el índice GINI, obteniendo información desde la API del Banco Mundial "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22".
La obtención de los datos se hará mediante el uso de API REST y Python, luego esos datos serán pasados a un programa en C que será el intermediario para hacer llamadas a rutinas de cálculos escritas en Assembler y luego de realizados los mismos, deben ser mostrados los resultados.
Los cálculos a realizar consisten en:

- Convertir de Float a Int.
- Al índice obtenido de la API sumarle (+1).
- Devolver el resultado para ser visualizado en pantalla.

Otro aspecto a tener en cuenta, es que sebe utilizar el STACK para convocar, enviar parámetros y devolver resultados.

## Librerias utilizadas en Python para la comunicación entre los procesos

- Librería "requests" para enviar solicitudes HTTP a servidores web y recibir respuestas.
- Librería "json" para poder trabajar con archivos JSON obtenidos luego de hacer solicitudes a los servidores web.
- Librería "ctypes"que permite cargar y llamar a funciones de librerías compartidas escritas en lenguajes como C o C++.
- Librería "numpy" para trabajar numéricamente con los arreglos de datos obtenidos.
- Librería "tkinter" para proporcionar una interfaz gráfica (GUI) y mostrar los resultados finales.



