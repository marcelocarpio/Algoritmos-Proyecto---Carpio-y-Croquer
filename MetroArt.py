from PIL import Image
import requests
from Departamento import Departamento
from Obra_Arte import ObraDeArte
from Artista import Artista

class MetroArt:   
    def db_inicial(self):
        resp= requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")
        return resp.json()
    def cargar_departamentos(self):
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
    def cargar_ids_por_departamento(self, id_departamento):
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
    def cargar_detalles_obra(self, id_obra):
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
    def paginacion_cargar_obras(self, id_departamento, limite=20):
        lista_ids = self.cargar_ids_por_departamento(id_departamento)

        ids_paginas = lista_ids[:limite]
        
        obras_encontradas = []    
        for id_obra in ids_paginas:
            obra = self.cargar_detalles_obra(id_obra)
            obras_encontradas.append(obra)
                
        return obras_encontradas

    def cargar_nacionalidades_lista(self):
        """
        Crea una lista de nacionalidades desde el archivo CSV.
        Retorna una lista con las nacionalidades.
        """
        nacionalidades = []
        with open('PROYECTO/lista_nacionalidades.csv', 'r') as lista_nacionalidades:

            for nacion in lista_nacionalidades:
                pais=nacion.strip()
                nacionalidades.append(pais)
        print("Lista de nacionalidades obtenida con éxito.")
        return nacionalidades

    def buscar_por_nacionalidad(self, nacionalidad):
        """
        Args: nacionalidad (str): La nacionalidad del autor a buscar.
        Returns: lista de IDs que coinciden con la nacionalidad.
        """
        intentos = 3
        while intentos > 0:
            resp = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={nacionalidad}")

            if resp.status_code == 200:
                nacionalidad_json = resp.json()
                ids_por_nacionalidad = nacionalidad_json.get("objectIDs", [])
                return ids_por_nacionalidad

            else:
                print(f"Error. Código de estado: {resp.status_code}. Intentos restantes: {intentos - 1}")
                intentos -= 1

        print(f"Error al cargar las obras de {nacionalidad}")
        return []

    def buscar_por_autor(self, autor):
        """
        Args: Nombre del autor (str): El nombre del autor a buscar.
        Returns: lista de IDs que coinciden con el autor.
        """
        intentos = 3
        while intentos > 0:
            resp = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={autor}")

            if resp.status_code == 200:
                autor_json = resp.json()
                ids_por_autor = autor_json.get("objectIDs", [])
                return ids_por_autor

            else:
                print(f"Error. Código de estado: {resp.status_code}. Intentos restantes: {intentos - 1}")
                intentos -= 1

        print(f"Error al cargar las obras de {autor}")
        return []

    def start(self):
        while True:
            opcion = input('''\tMenu
1. Buscar Obras
2. Mostrar detalles de una obra
3. Salir
>>>''')
            if opcion == '1':
                opcion1 = input('''\tMenu
1. Buscar Obras por Departamento
2. Buscar Obras por Nacionalidad del autor
3. Mostrar Obras por nombre del autor
>>>''')
                if opcion1 == '1':
                    self.busqueda_dpto()
                elif opcion1 == '2':
                    self.busqueda_nacionalidad()
                elif opcion1 == '3':
                    self.busqueda_autor()

            elif opcion == '2':
                self.mostrar_detalles_y_imagen

            elif opcion == '3':
                print('Saliendo...')
                break
            else:
                print('Opción inválida. Intente nuevamente')

    def busqueda_dpto(self):
        lista_dptos = sorted(self.cargar_departamentos(),key = lambda x: x.id)
        print('-'*30)
        for dpto  in lista_dptos:
            print(f'{dpto.id}. {dpto.nombre}')
        print('-'*30)
        id_dpto = input('Ingrese el Id del Departamento: ').strip()
        obras = self.cargar_ids_por_departamento(id_dpto)

        if not obras:
            print("No se encontraron obras para este departamento.")
        else:
            for id_obra in obras[:20]:
                obra = self.cargar_detalles_obra(id_obra)
                obra.resumen()

    def busqueda_nacionalidad(self):
        lista_nacionalidades = self.cargar_nacionalidades_lista()
        print('-'*30)
        for nacionalidad in lista_nacionalidades:
            print(nacionalidad)
        print('-'*30)
        nacionalidad = input("Ingrese la nacionalidad del autor: ").strip().capitalize()
        print()
        ids_nacionalidad = self.buscar_por_nacionalidad(nacionalidad)
        if not ids_nacionalidad:
            print("No se encontraron obras para esta nacionalidad.")
        else:
            for id_obra in ids_nacionalidad[:20]:
                obra = self.cargar_detalles_obra(id_obra)
                obra.resumen()

    def busqueda_autor(self):
        nombre_autor = input("Ingrese el nombre del autor: ").strip().capitalize()
        ids_autor = self.buscar_por_autor(nombre_autor)

        if not ids_autor:
            print("No se encontraron obras para este autor.")
        else:
            for id_obra in ids_autor[:20]:
                obra = self.cargar_detalles_obra(id_obra)
                obra.resumen()

    def mostrar_detalles_y_imagen(self):
        id_obra = input("Ingrese el ID de la obra: ").strip()
        obra = self.cargar_detalles_obra(id_obra)
        if obra:
            obra.mostrar_detalles()
            if obra.url_imagen:
                try:
                    img = Image.open(requests.get(obra.url_imagen, stream=True).raw)
                    img.show()
                except Exception as e:
                    print(f"No se pudo mostrar la imagen: {e}")
        else:
            print("No se encontraron detalles para esta obra.")
