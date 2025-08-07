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
        try:
            with open('PROYECTO\lista_nacionalidades.csv', 'r') as lista_nacionalidades:

                for nacion in lista_nacionalidades:
                    pais=nacion.strip()
                    nacionalidades.append(pais)
            print("Lista de nacionalidades obtenida con éxito.")
            return nacionalidades
        except FileNotFoundError:
            print("El archivo lista_nacionalidades.csv no se encontró. Verifique la ruta del archivo")
            return []

        
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
        """        
        Inicia el programa y muestra el menú principal.
        """
        print("Bienvenido a MetroArt")
        while True:
            opcion = input('''\tMenu
1. Buscar Obras
2. Mostrar detalles de una obra
3. Salir
>>>''')
            if opcion == '1':
                opcion1 = input('''\tOpciones de búsqueda
1. Buscar Obras por Departamento
2. Buscar Obras por Nacionalidad del autor
3. Mostrar Obras por nombre del autor
>>>''')
                if opcion1 == '1':
                    self.busqueda_dpto()
                    print()
                elif opcion1 == '2':
                    self.busqueda_nacionalidad()
                    print()
                elif opcion1 == '3':
                    self.busqueda_autor()
                    print()

            elif opcion == '2':
                self.mostrar_detalles_y_imagen()
                print()

            elif opcion == '3':
                print('Saliendo...')
                break
            else:
                print('Opción inválida. Intente nuevamente')

    def validar_id(self, input_str, lista_ids):
        """
        Valida que el input sea un número entero que esté en la lista de IDs válidos.

        Args:
            input_str (str): Entrada del usuario.
            lista_ids (list[int]): Lista de IDs válidos.

        Returns:
            int | None: Valor entero si es válido, o None si hay error.
        """
        try:
            valor = int(input_str.strip())
        except ValueError:
            print("[ERROR] Debe ingresar un número entero válido.")
            return None

        if valor not in lista_ids:
            print(f"[ERROR] El ID ingresado ({valor}) no existe.")
            return None

        return valor
    
    def mostrar_seguro(self, obra, metodo="resumen"):
        if obra and hasattr(obra, metodo):
            try:
                obra.resumen()
            except:
                print(f"No se pudo mostrar el resumen de la obra {obra.id}.")
        else:
            print(f"[WARNING] Obra inválida o sin método '{metodo}'.")
    
    def busqueda_dpto(self):
        """
        Busca las obras por departamento utilizando la función cargar_departamentos.
        Muestra una lista de departamentos y permite al usuario seleccionar uno.
        """
        lista_dptos = sorted(self.cargar_departamentos(),key = lambda x: x.id)
        print('-'*30)
        for dpto  in lista_dptos:
            print(f'{dpto.id}. {dpto.nombre}')
        print('-'*30)

        id_dpto = input('Ingrese el Id del Departamento: ')
        ids_disponibles = [d.id for d in lista_dptos]
        id_valido = self.validar_id(id_dpto, ids_disponibles)

        if id_valido is None:
            return  
        print()
        obras = self.cargar_ids_por_departamento(id_dpto)

        if not obras:
            print("No se encontraron obras para este departamento.")
            return

        index = 0
        while index < len(obras):
            for id_obra in obras[index:index+20]:
                obra = self.cargar_detalles_obra(id_obra)
                if obra is None:
                    print("Se detiene la búsqueda por fallo en la API.")
                    return
                self.mostrar_seguro(obra)

            index += 20
            if index >= len(obras):
                break
            print()
            opcion = input("""¿Mostrar más obras?
1. Sí  
2. No
>>> """)
            print()
            if opcion.strip() != '1':
                break

    def busqueda_nacionalidad(self):
        """
        Busca las obras por nacionalidad utilizando la función cargar_nacionalidades_lista.
        Muestra una lista de nacionalidades y permite al usuario seleccionar una.
        """
        lista_nacionalidades = self.cargar_nacionalidades_lista()
        print('-'*30)
        for nacionalidad in lista_nacionalidades:
            print(nacionalidad)
        print('-'*30)
        nacionalidad = input("Ingrese la nacionalidad del autor: ").strip().capitalize()
        print()
        ids = self.buscar_por_nacionalidad(nacionalidad)

        if not ids:
            print("No se encontraron obras para esta nacionalidad.")
            return

        index = 0
        while index < len(ids):
            for id_obra in ids[index:index+20]:
                obra = self.cargar_detalles_obra(id_obra)
                if obra is None:
                    print("Se detiene la búsqueda por fallo en la API.")
                    return
                self.mostrar_seguro(obra)

            index += 20
            if index >= len(ids):
                break
            print()
            opcion = input("""¿Mostrar más obras?
1. Sí  
2. No
>>> """)
            print()
            if opcion.strip() != '1':
                break

    def busqueda_autor(self):
        nombre_autor = input("Ingrese el nombre del autor: ").strip().capitalize()
        ids_autor = self.buscar_por_autor(nombre_autor)

        if not ids_autor:
            print("No se encontraron obras para este autor.")
            return

        index = 0
        while index < len(ids_autor):
            for id_obra in ids_autor[index:index+20]:
                obra = self.cargar_detalles_obra(id_obra)
                if obra is None:
                    print("Se detiene la búsqueda por fallo en la API.")
                    return
                self.mostrar_seguro(obra)

            index += 20
            if index >= len(ids_autor):
                break
            print()
            opcion = input("""¿Mostrar más obras?
1. Sí  
2. No
>>> """)
            print()
            if opcion.strip() != '1':
                break

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
