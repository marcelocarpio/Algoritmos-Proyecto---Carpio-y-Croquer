import time
import requests
from PIL import Image
from io import BytesIO
from api_mueso import *

def busqueda_dpto():
    lista_dptos = sorted(cargar_departamentos(),key = lambda x: x.id)
    print('-'*30)
    for dpto  in lista_dptos:
        print(f'{dpto.id}. {dpto.nombre}')
    print('-'*30)
    id_dpto = input('Ingrese el Id del Departamento: ').strip()
    obras = cargar_ids_por_departamento(id_dpto)

    if not obras:
        print("No se encontraron obras para este departamento.")
    else:
        for id_obra in obras[:20]:
            obra = cargar_detalles_obra(id_obra)
            print(f"{obra.id}: {obra.titulo} - {obra.artista.nombre}")

def busqueda_nacionalidad():
    lista_nacionalidades = cargar_nacionalidades_lista()
    for nacionalidad in lista_nacionalidades:
        print(nacionalidad)
    nacionalidad = input("Ingrese la nacionalidad del autor: ").strip()

    obras_encontradas = []

    for id_obra in range(1, 200):
        obra = cargar_detalles_obra(id_obra)
        if obra.artista.nacionalidad.lower() == nacionalidad.lower():
            obras_encontradas.append(obra)
    for obra in obras_encontradas:
            print(f"{obra.id}: {obra.titulo} - {obra.artista.nombre}")

def busqueda_autor():
    nombre_autor = input("Ingrese el nombre del autor: ").strip().lower()
    obras_encontradas = []

    for id_obra in range(1, 200):
        obra = cargar_detalles_obra(id_obra)
        if nombre_autor in obra.artista.nombre.lower():
            obras_encontradas.append(obra)

    if not obras_encontradas:
        print("No se encontraron obras para este autor.")
    else:
        for obra in obras_encontradas:
            print(f"{obra.id}: {obra.titulo} - {obra.artista.nombre}")

busqueda_autor()
