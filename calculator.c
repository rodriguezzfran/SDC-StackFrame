#include <stdio.h>
#include <stdlib.h>  // Para NULL
#include <dlfcn.h>   // Para cargar librerías dinámicas

typedef int (*plus_one_func)(int);

void plus_one(float* array, int size) {
    // Cargar la librería de ensamblador
    
    void* handle = dlopen("./libcalc_asm.so", RTLD_LAZY);
    if (handle == NULL) {
        fprintf(stderr, "Error al cargar la librería de ensamblador\n");
        return -1;
    }

    // Cargar la función de ensamblador
    plus_one_func plus_one_asm = (plus_one_func) dlsym(handle, "plus_one_asm");
    
    // Verificar si la función fue cargada correctamente
    if (plus_one_asm == NULL) {
        fprintf(stderr, "Error al cargar la función de ensamblador\n");
        dlclose(handle);
        return -1;
    }

    // Llamar a la función de ensamblador
    for (int i = 0; i < size; i++) {
        array[i] = (float)plus_one_asm((int)array[i]);
    }

    dlclose(handle);  // Cerrar la librería después de usarla
}
