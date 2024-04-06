#include <stdio.h>

// La función que será llamada desde Python
int average_plus_one(float* array) {
    float sum = 0;
    int size = sizeof(array) / sizeof(array[0]);
    for (int i = 0; i < size; i++){
        sum += array[i];
    }
    int average = sum / size;
    return average + 1;
}