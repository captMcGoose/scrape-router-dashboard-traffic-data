#Este es para los datos transmitidos. Mismo codigo, pero buscamos la columna 9 en vez de la 1. 

import requests
from bs4 import BeautifulSoup
import csv
import time
import datetime

# Credenciales del Dashboard del router
router_ip = '192.168.0.1'  # IP del router
password = 'password'  # Contraseña del dashboard del router

# Abrimos un session
session = requests.Session()

# Abrimos el csv
with open('datosRouterTrans.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Data'])

    # Repetimos 24 veces por cada hora
    for i in range(24):
        # Mandamos un POST con la contraseña al querry "Password"
        login_data = {'Password': password}
        login_response = session.post(f'http://{router_ip}', data=login_data)

        # La tabla se encuentra en statsifc.html, Y solamente contiene una simple tabla HTML. Mas simple y pobre no podria ser. No tiene ni un id. 
        statistics_page = session.get(f'http://{router_ip}/statsifc.html')
        soup = BeautifulSoup(statistics_page.content, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')
        #vamos a sumar todos los valores de todos los eth.
        extractedNumber = int(rows[6].find_all('td')[9].text) + int(rows[7].find_all('td')[9].text) + int(rows[8].find_all('td')[9].text) + int(rows[9].find_all('td')[9].text) + int(rows[10].find_all('td')[9].text) + int(rows[12].find_all('td')[9].text) 

        # Obtenemos el time stamp actual
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Añadimos erl timestamp y el dato al csv
        writer.writerow([timestamp, extractedNumber])

        # esperamos 1h
        time.sleep(3600)

    
