import requests #Importamos la librería requests para hacer solicitudes HTTP
import json #Importamos la librería json para trabajar con archivos JSON
import ctypes #Importamos la librería ctypes que nos deja mandar la informacion a el programa en c
import numpy as np #Importamos la librería numpy para trabajar con arreglos de datos
from tkinter import Tk, Label, Button,ttk #Importamos la librería tkinter para crear una interfaz gráfica
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# URL de la API a dónde vamos a hacer las solicitudes 
URL = 'https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22'

#Cargamos la libreria de C
calculator = ctypes.CDLL('./build/libcalc.so')

#Definimos el tipo de dato que vamos a usar en la biblioteca
calculator.plus_one.argtypes = [ctypes.POINTER(ctypes.c_float),ctypes.c_int]
calculator.plus_one.restype = ctypes.POINTER(ctypes.c_int)

#funcion GET para traer datos de la API
def get_data():
    response = requests.get(URL) #Hacemos la solicitud GET a la URL
    
    #el codigo 200 indica que la solicitud fue exitosa
    if response.status_code == 200:
        print('Success!')
        data = response.json() #Convertimos la respuesta a JSON para mejor legibilidad
        return data #devuelve la data al main
    else:
        print('Error')
        return None

#funcion para filtrar la data por pais    
def filter_country(data, country):
    filtered_data = [] #Creamos una lista vacía para guardar la data filtrada segun pais
    
    #Iteramos sobre la data y si el item tiene la clave 'country' y la clave 'id' y el valor de 'id' es igual al pais, lo agregamos a la lista
    for item in data:
        if 'country' in item and 'id' in item['country'] and item['country']['id'] == country:
            filtered_data.append(item)
    return filtered_data

#funcion para filtrar los valores de la data
def filter_values(data):
    values = []
    years = []  # Lista para guardar los años
    for item in data:
        if 'value' in item and 'date' in item:
            if item['value'] is not None:
                values.append(item['value'])
                years.append(item['date'])  # Guardar el año correspondiente a cada valor
    return values[::-1], years[::-1]  # Devolver los valores y los años en orden cronológico

def update_label(result, years, label):
    # Limpiar los ejes existentes
    canvas.figure.clear()
    ax = canvas.figure.subplots()

    # Dibujar el gráfico
    ax.plot(years, result, marker='o')
    ax.set_xlabel('Año')
    ax.set_ylabel('Índice GINI')
    ax.set_title('Índice GINI a lo largo del tiempo')

    # Redibujar el gráfico
    canvas.draw()

#funcion para crear la interfaz grafica
def on_button_click(label, country_code):
    if not country_code:
        label.config(text="Seleccionar un país")
        return
    data = get_data() #Obtenemos la data de la API
    if data: #Si la data no es None
        filtered_data = filter_country(data[1], country_code)
        values, years = filter_values(filtered_data)  # Obtener los valores y los años
        values = np.array(values, dtype=np.float32)
        
        result = calculator.plus_one(values.ctypes.data_as(ctypes.POINTER(ctypes.c_float)), len(values))
        result = np.ctypeslib.as_array(result, (len(values),))  # Convertir el resultado a un array de numpy
        
        update_label(result, years, label)
    else:
        label_result['text'] = 'No hay información disponible' #Si la data es None, imprimimos un mensaje de error

def create_gui():
    root = Tk() #Creamos una ventana
    root.title('Calculadora GINI') #Le ponemos un título a la ventana
   # Cambiando el color de fondo de la ventana
    root.configure(bg='#f0f0f0')

    result_label = Label(root, bg='#f0f0f0')
    result_label.pack()

    # Combobox para seleccionar el país
    country_label = Label(root, text="Seleccionar país:", bg='#f0f0f0')
    country_label.pack()
    country_combobox = ttk.Combobox(root, values=["AR", "BR", "CL", "UY","PY","US","IT","ES"])  # Se pueden agregar más códigos de paises
    country_combobox.pack()

    # Botón que al presionarlo actualizará la etiqueta
    request_button = Button(root, text="Solicitar Datos", command=lambda: on_button_click(result_label,country_combobox.get()), bg='#007bff', fg='white', font=('Helvetica', 12))
    request_button.pack()

    # Crea el objeto canvas para poder hacer dinámicos los gráficos
    global canvas
    fig = plt.Figure(figsize=(6, 5), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=result_label)
    canvas.get_tk_widget().pack()

    root.mainloop() #Iniciamos el loop de la ventana


#funcion principal
def main():
    create_gui() #Invocamos la interfaz

#esto asegura que se llame el main cuando se ejecute el script
if __name__ == "__main__":
    main()
