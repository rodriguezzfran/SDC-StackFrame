import requests #Importamos la librería requests para hacer solicitudes HTTP
import json #Importamos la librería json para trabajar con archivos JSON

# URL de la API a dónde vamos a hacer las solicitudes 
URL = 'https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22'

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
    
def filter_country(data, country):
    filtered_data = []
    for item in data:
        if 'country' in item and 'id' in item['country'] and item['country']['id'] == country:
            filtered_data.append(item)
    return filtered_data

def filter_values(data):
    values = []
    for item in data:
        if 'value' in item:
            if item['value'] is None:
                values.append(0)
            else:
                values.append(item['value'])
    return values

#funcion principal
def main():
    data = get_data() #Obtenemos la data de la API
    if data: #Si la data no es None
        filtered_data = filter_country(data[1], 'AR')
        values = filter_values(filtered_data)
        
    else:
        print('No data available') #Si la data es None, imprimimos un mensaje de error

#esto asegura que se llame el main cuando se ejecute el script
if __name__ == "__main__":
    main()