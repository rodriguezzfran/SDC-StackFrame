#include <stdio.h>
#include <stdlib.h>  // Para NULL
#include <dlfcn.h>   // Para cargar librerías dinámicas

typedef int (*plus_one_func)(int);

int* plus_one(float* array, int size) {
    // Cargar la librería de ensamblador
    void* handle = dlopen("../build/libcalc.so", RTLD_LAZY);
    if (handle == NULL) {
        fprintf(stderr, "Error al cargar la librería de ensamblador\n");
        return NULL;
    }

    // Cargar la función de ensamblador
    int (*add_one)(int) = dlsym(handle, "add_one");
    char* error = dlerror();
    if (error) {
        fputs(error, stderr);
        return NULL;
    }

    // Verificar si la función fue cargada correctamente
    if (add_one == NULL) {
        fprintf(stderr, "Error al cargar la función de ensamblador\n");
        dlclose(handle);
        return NULL;
    }

    // Crear un nuevo array de enteros
    int* new_array = (int*) malloc(size * sizeof(int));
    if (new_array == NULL) {
        fprintf(stderr, "Error al asignar memoria para el nuevo array\n");
        dlclose(handle);
        return NULL;
    }

    // Llamar a la función de ensamblador y almacenar el resultado en el nuevo array
    for (int i = 0; i < size; i++) {
        new_array[i] = add_one((int)array[i]);
    }

    dlclose(handle);  // Cerrar la librería después de usarla

    return new_array;  // Devolver el nuevo array
}
