section .data
    num dd 0

section .text
    global average_plus_one_asm

average_plus_one_asm:

    ; Parámetros:
    ;   - [rdi]: Dirección base del array (puntero al primer elemento)
    ;   - [rsi]: Tamaño del array (cantidad de elementos)
    ; Devuelve el resultado en rax

    xor rax, rax        ; Inicializamos el acumulador en 0
    mov rcx, rsi        ; Cargamos el tamaño del array en rcx

    ; Bucle para sumar los valores del array
    suma_loop:
        cvtss2si r8, [rdi+rcx*4-4]  ; Convertimos float a int
        add rax, r8                ; Sumamos el valor actual al acumulador
        loop suma_loop

    ; Calculamos el promedio
    cqo                 ; Extendemos el acumulador a rdx:rax
    idiv rsi            ; Dividimos rdx:rax por el tamaño del array

    ; Sumamos 1 al resultado
    add rax, 1

    ret

    
