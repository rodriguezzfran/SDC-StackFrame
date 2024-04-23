#include <stdio.h>
#include <stdlib.h>  // Para NULL
#include <dlfcn.h>   // Para cargar librerías dinámicas

typedef int (*average_plus_one_func)(float*, int);

int average_plus_one(float* array, int size) {
    // Cargar la librería de ensamblador
    
    void* handle = dlopen("./libcalc_asm.so", RTLD_LAZY);
    if (handle == NULL) {
        fprintf(stderr, "Error al cargar la librería de ensamblador\n");
        return -1;
    }

    // Cargar la función de ensamblador
    average_plus_one_func average_plus_one_asm = (average_plus_one_func) dlsym(handle, "average_plus_one_asm");
    
    // Verificar si la función fue cargada correctamente
    if (average_plus_one_asm == NULL) {
        fprintf(stderr, "Error al cargar la función de ensamblador\n");
        dlclose(handle);
        return -1;
    }

    // Llamar a la función de ensamblador
    printf("el contenido del array es: \n");
    for (int i = 0; i < size; i++) {
        printf("%f\n", array[i]);
    }

    int result = average_plus_one_asm(array, size);
    

    dlclose(handle);  // Cerrar la librería después de usarla
    
    return result;
}
