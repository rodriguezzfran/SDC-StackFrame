section .data
    num dd 0

section .text
global add_one

add_one:
    ; Configurar el stack frame
    push rbp          ; Guardar el frame actual
    mov rbp, rsp      ; Establecer rbp para acceder al stack
    
    ; Acceder al primer argumento (está a 16 bytes de rbp debido a la dirección de retorno y rbp)
    mov eax, dword [rbp + 16]
    
    ; Sumar uno al valor de entrada
    add eax, 1
    
    ; Devolver el resultado en eax (o rax para 64 bits)
    mov rax, rdi      ; Devolver el resultado al llamador
    
    ; Restaurar el stack frame
    pop rbp           ; Restaurar rbp
    ret               ; Retornar al llamador


    
