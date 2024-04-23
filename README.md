# SdC 2024 - Trabajo Práctico N° 2

## Introducción

El objetivo del siguiente trabajo es diseñar e implementar una interfaz que muestre el índice GINI del país requerido, obteniendo información desde la API del Banco Mundial "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22".
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

## Pasos de funcionamiento de la aplicación
1. Se cargan las librerias.
2. Se define el tipo de dato requerido para los datos de la API.
3. Se hace la solicitud de datos a la URL del banco mundial. 
4. Se verifica que la solicitud haya sido exitosa.
5. Obtenidos los datos, se filtran por el país nombre del país deseado.
6. Se abre la GUI donde se le da al usuario la opción de mostrar el índice GINI.
7. Si el usuario decide obtener el valor de índice, se llama a la función "calculator" escrita en C para la conversión de tipo de dato y agregarle +1.
8. Se muestra el resultado en la ventana gráfica.

## Imágenes funcionando

<p align="center">
  <img src="/pictures/solicitud.png" alt="Posibles solicitudes del índice GINI">
</p>

<p align="center">
  <img src="/pictures/respuesta.png" alt="Valor del índice GINI según el país seleccionado">
</p>



## Para compilar y correr el programa, tener instalado los paquetes:
- nasm 
```bash
sudo apt-get install nasm gcc-multilib g++-multilib
```
- cmake 
```bash
sudo apt install cmake
```
- numpy
```bash
pip install numpy
```
- tkinter
```bash
sudo apt install python3-tk
```

En la carpeta raíz del repositorio ejecutar los siguientes comandos:

```bash
mkdir build
cd build
cmake ..
make
cd ..
python3 GINI_interface.py
```
## PARTE 2
Para la parte 2 se incorporó una llamada a Assembler desde la función de C, el objetivo es desde Pyhton se haga una llamada a una función en C, luego esta función en C llamará a una en Assembler habiendole pasado un puntero a un array, la función en Assembler se encargará de usar el stack frame para acceder a los parámetros, convertir los elementos del array a int, sumarlos, sacar el promedio y sumarle uno, para luego ser devuelto a C, quién los volverá a enviar a Python

### Como instalar
Para poder ejecutar este nuevo programa debemos usar los siguiente comandos.

Una vez tengamos el código en assembler en un `.asm` debemos compilarla para crear una librería compartida (.so)

```bash
nasm -f elf64 -o average_plus_one.o average_plus_one.asm
gcc -shared -o libcalc_asm.so average_plus_one.o
```
Una vez tenemos la librería compartida para C, repetimos el proceso para crear una librería compartida para Python

```bash
gcc -shared -o libcalc.so calculator.c -ldl
```
Finalmente abrimos el código creado para python utilizando el siguiente comando

```bash
python3 GINI_interface.py
```


