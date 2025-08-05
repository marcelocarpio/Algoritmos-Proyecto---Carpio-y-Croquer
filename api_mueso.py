import requests
from Departamento import Departamento
from Obra_Arte import ObraDeArte
from Artista import Artista

def db_inicial():
    resp= requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")
    return resp.json()

def cargar_departamentos():
    """
    Obtiene la lista de departamentos del museo y los convierte en objetos.
    Retorna una lista de objetos Departamento.
    """
    
    intentos=3
    while intentos > 0:
        resp= requests.get("https://collectionapi.metmuseum.org/public/collection/v1/departments")

        if resp.status_code == 200:
            datos_json = resp.json()
            departamentos_list = []
            dic_datos=datos_json.get("departments")

            for dato in dic_datos:
                departamentos_list.append(Departamento(dato["departmentId"],dato["displayName"], []))

            print("Departamentos obtenidos con éxito.")
            return departamentos_list
            
        else:
            print(f"Intento fallido. Código de estado: {resp.status_code}. Intentos restantes: {intentos - 1}")
            intentos -= 1
    
    print("No se pudo obtener la lista de departamentos.")
    return []

def cargar_ids_por_departamento(id_departamento):
    """
    IDs de las obras para un departamento específico.
    Retorna una lista de IDs de las obras.
    
    Args:
        departamento_id (int): El ID del departamento.
    """

    intentos = 3
    while intentos > 0:
        resp = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds={id_departamento}")

        if resp.status_code == 200:
            ids_json = resp.json()
            lista_ids_obras=(ids_json.get("objectIDs"))
            print(f"Se encontraron {len(lista_ids_obras)} obras para el departamento {id_departamento}.")
            return lista_ids_obras
        
        else:
            print(f"Error. Código de estado: {resp.status_code}. Intentos restantes: {intentos - 1}")
            intentos -= 1
            
    print(f"No se pudo obtener la lista de IDs.")
    return []

def cargar_detalles_obra(id_obra):
    """
    Obtiene los detalles de una obra y crea un objeto Artista y un objeto ObraDeArte.
    
    Args:
        id_obra (int): El ID de la obra de arte.
    """
    intentos = 3
    while intentos > 0:
        resp = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{id_obra}")
        
        if resp.status_code == 200:
            id_obra_json = resp.json()
            
            artista = Artista(nombre=id_obra_json.get("artistDisplayName", "Desconocido"), nacionalidad=id_obra_json.get("artistNationality", "Desconocida"), nacimiento=id_obra_json.get("artistBeginDate", "Desconocida"),  muerte=id_obra_json.get("artistEndDate", "Desconocida"))

            obra = ObraDeArte(id=id_obra_json.get("objectID", None), titulo=id_obra_json.get("title", "Desconocido"), artista=artista, clasificacion=id_obra_json.get("classification", "Desconocida"), anio=id_obra_json.get("objectDate", "Desconocida"), url_imagen=id_obra_json.get("primaryImage"))
            if obra.id==None:
                print(f"No se obtuvo el ID de la obra {obra.name}")
            return obra
        
        else:
            print(f"Error. Código de estado: {resp.status_code}. Intentos restantes: {intentos - 1}")
            intentos -= 1
            
    print(f"No se pudieron obtener los detalles de la obra {id_obra}.")
    return None


def paginacion_cargar_obras(id_departamento, limite=20):
    lista_ids = cargar_ids_por_departamento(id_departamento)
    
    ids_paginas = lista_ids[:limite]
    
    obras_encontradas = []    
    for id_obra in ids_paginas:
        obra = cargar_detalles_obra(id_obra)
        obras_encontradas.append(obra)
            
    return obras_encontradas


def cargar_nacionalidades_lista():
    """
    Crea una lista de nacionalidades desde el archivo CSV.
    Retorna una lista con las nacionalidades.
    """
    nacionalidades = []
    with open('lista_nacionalidades.csv', 'r') as lista_nacionalidades:
        
        for nacion in lista_nacionalidades:
            pais=nacion.strip()
            nacionalidades.append(pais)
    print("Lista de nacionalidades obtenida con éxito.")
    return nacionalidades
