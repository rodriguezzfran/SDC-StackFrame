section .text
global add_one      ; Declara la función como global para que pueda ser llamada desde C

; Entradas:
;   rdi - Parámetro de entrada (entero a sumar)
; Salidas:
;   rax - Resultado (suma + 1)
add_one:
    ; Guardar el registro rdi (parámetro de entrada)
    push rdi

    ; Sumar 1 al parámetro de entrada (rdi)
    inc rdi

    ; Mover el resultado a rax (registro de retorno)
    mov rax, rdi

    ; Restaurar el registro rdi
    pop rdi

    ; Retornar a la función llamadora
    ret
