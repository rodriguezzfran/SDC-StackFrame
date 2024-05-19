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
nasm -f elf64 -o Calculator_ASM.o Calculator_ASM.asm
gcc -shared -o libca.o
```
Una vez tenemos la librería compartida para C, repetimos el proceso para crear una librería compartida para Python

```bash
gcc -shared -o libcalc.so calculator.c -ldl
```
Finalmente abrimos el código creado para python utilizando el siguiente comando

```bash
python3 GINI_interface.py
```
## NUEVA VERSIÓN
Luego de los cambios solicitados en la clase con el profesor Javier Jorge se implementaron algunas modificaciones a la forma en la cual el programa responde así como también una mejor interfaz con algunas consideraciones adicionales.

### Esquema de directorios actualizados
Se añadieron 2 scripts que ayudarán a hacer una instalación mucho más limpia y ordenada

build.sh permitirá crear la carpeta *build* a partir de los archivos fuente en *src*, de esta manera nos independizamos de saber los comandos

```sh
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
````
Luego el script de *run.sh* permitirá correr la interfáz gráfica que llama a las funciones hechas en *C* y *Assembler* desde la carpeta *build*
```bash
#!/bin/bash

# Comprobar si la carpeta build existe
if [ -d "build" ]; then
    # Si existe, ejecutar el programa en Python
    python3 src/GINI_interface.py
else
    # Si no existe, imprimir un mensaje de error
    echo "Error: la carpeta build no existe. Por favor, ejecuta el script de build primero."
fi
````
### Nueva interfaz y cambio de la función en assembler

El calculo anterior estaba mal, así que fué cambiado a una nueva versión, la cual ahora responde al siguiente flujo:
- Cuándo el usuario hace click en el botón de "Solicitar datos" se llama a la función __*get_data()*__ mediante un __*on_button_click*__ que obtiene los datos de la API
- Una vez obtenidos los datos estos en formato *__JSON__* se filtran los datos para incluir sólo aquellos que son del país solicitado en la interfaz
- Se extraen los los valores del índice GINI y el año de cada valor
- Se crea una lista separa para los valores y los años, eliminando entradas nulas
- Utilizando la función hecha en *__C__* los datos se convierten a un array de tipo *__ctypes.c_float__* y se pasa el tamaño del array como parámetro para esta función
- La función en C *__"plus_one"__* recorre el array pasado como parámetro y utilizando un puntero a la función en *__Assembler__* se le pasa cada valor individual
- La función en *__Assembler__* se encarga de obtener el valor, sumarle 1 y devolverlo al array en *__C__*
- Una vez que se actualizaron todos los datos estos se plasman en la interfaz de *__python__*

![image](https://github.com/rodriguezzfran/SDC-StackFrame/assets/122646722/ddb125cf-5ba1-4420-bdb9-ae135dc7182e)

### Impresión del stack
Para poder ver el stack utilizaremos *__gdb__*, la única diferencia es que debemos compilar utilizando la flag *__-g__* asi que hicimos un nuevo script que permite esta posibilidad
```sh
#!/bin/bash

# Borrar la carpeta build si existe
if [ -d "build" ]; then
    rm -r build
fi

# Crear la carpeta build
mkdir build

# Compilar el código de ensamblador
nasm -f elf64 -g -o build/add_one.o src/Calculator_ASM.asm

# Compilar el código C
gcc -c -g -fPIC -o build/libcalc.o src/calculator.c

# Enlazar los archivos objeto para crear la biblioteca compartida
gcc -shared -o build/libcalc.so build/libcalc.o build/add_one.o
````
Una vez utilizado utilizamos el siguiente comando para iniciar el depurador]
```bash
gdb --args python3 GINI_interface.py
````
ahora debemos detenernos en el momento en el cual se llama a la función en assembler
````bash
break calculator.c:40
````
una vez que demos a run y el programa se frene tendremos que poner un breakpoint en la linea de assembler luego de que se pushee el parámetro al stack
```bash
break src/Calculator_ASM.asm:11
```
vemos que una vez alcanzado este punto el parámetro ya está pusheado en la pila

```bash
(gdb) break src/Calculator_ASM.asm:11
No hay un archivo fuente con el nombre src/Calculator_ASM.asm.
Make breakpoint pending on future shared library load? (y or [n]) y
Punto de interrupción 1 (src/Calculator_ASM.asm:11) pendiente.
(gdb) run
Starting program: /usr/bin/python3 GINI_interface.py
Downloading separate debug info for /lib/x86_64-linux-gnu/libz.so.1                                                                                  
[Depuración de hilo usando libthread_db enabled]                                                                                                     
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[Nuevo Thread 0x7ffff2e986c0 (LWP 13562)]                                                                                                            
Success!                                                                                                                                             

Thread 1 "python3" hit Breakpoint 1, add_one () at src/Calculator_ASM.asm:13
13          inc rdi
```
ahora con el siguiente comando podemos ver el stack

```bash
(gdb) info registers
rax            0x2a                42
rbx            0x1e36a00           31681024
rcx            0x0                 0
rdx            0x7ffff5302320      140737306960672
rsi            0x1e84910           32000272
rdi            0x2a                42
rbp            0x7fffffffc2a0      0x7fffffffc2a0
rsp            0x7fffffffc240      0x7fffffffc240
r8             0x7ffff53013f0      140737306956784
r9             0x0                 0
r10            0x7ffff53013d8      140737306956760
r11            0x1ad51e0           28135904
r12            0x7fffffffc460      140737488340064
r13            0x7fffffffc540      140737488340288
r14            0x7fffffffc360      140737488339808
```
Dónde podemos observar que *__0x2a__* a *__rdi__* con su valor

también podemos verificar la dirección de retorno y el valor que devolverá

```bash
(gdb) x/gx $rsp
0x7fffffffc240: 0x000000000000002a
```
