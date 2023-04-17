
#? Importar las librerías y dependencias a usar
import itertools
import pandas as pd
import numpy as np
from collections import Counter
import json


#? Importar el archivo sorteos.json y guardarlo dentro de la variable "data"
with open('sorteos.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


#? Aquí le indicamos la cantidad de números que queremos ver si se repiten
numeros_repitidos_a_buscar = 3  # Aquí puede cambiar el valor entre 3 y 7.
assert 3 <= numeros_repitidos_a_buscar <= 7, "El número debe estar entre 3 y 7."


#? Aquí iteramos comparando todos los array dentro de cada diccionario
combinaciones = {}
for idx1, dic1 in enumerate(data):
    for idx2, dic2 in enumerate(data):
        if idx1 == idx2:
            continue
        
        key1, numeros1 = list(dic1.items())[0]
        key2, numeros2 = list(dic2.items())[0]

        comun = set(numeros1).intersection(numeros2)
        for comb in itertools.combinations(comun, numeros_repitidos_a_buscar):
            combinaciones[comb] = combinaciones.get(comb, set())
            combinaciones[comb].add(key1)
            combinaciones[comb].add(key2)


#? Crear un diccionario de combinaciones para cada cantidad de repeticiones
combinaciones_por_repeticion = {}
for comb, fechas in combinaciones.items():
    repeticiones = len(fechas)
    combinacion_numeros = ', '.join(map(str, comb))
    fechas_str = ', '.join(sorted(fechas))
    combinaciones_por_repeticion[repeticiones] = combinaciones_por_repeticion.get(repeticiones, [])
    combinaciones_por_repeticion[repeticiones].append((combinacion_numeros, fechas_str))


#? Generar el archivo Excel con los resultados agrupados por cantidad de repeticiones
if combinaciones:
    excel_data = []
    for repeticiones in sorted(combinaciones_por_repeticion.keys(), reverse=True):
        excel_data.append([f"Se repiten {repeticiones} veces las siguientes combinaciones:"])
        for combinacion_numeros, fechas_str in combinaciones_por_repeticion[repeticiones]:
            excel_data.append([f"La combinación de números {combinacion_numeros}"])
            excel_data.append([f"Las fechas en las que se repite la combinación de números anterior son las siguientes: {fechas_str}"])
            excel_data.append([""])

    df = pd.DataFrame(excel_data)
    df.to_excel("combinaciones.xlsx", index=False, header=False, engine='openpyxl')
else:
    print(f"No se ha encontrado que al menos {numeros_repitidos_a_buscar} números se repitan a lo largo de las fechas ingresadas.")