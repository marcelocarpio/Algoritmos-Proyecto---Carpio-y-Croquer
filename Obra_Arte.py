class ObraDeArte:
    def __init__(self, id, titulo, artista, clasificacion, anio, url_imagen):
        self.id=id
        self.titulo=titulo
        self.artista=artista
        self.clasificacion=clasificacion
        self.anio=anio
        self.url_imagen=url_imagen

    def resumen(self):
        print(f"{self.id}: {self.titulo} - {self.artista.nombre}")

    def mostrar_detalles(self):
        print(f"ID: {self.id}")
        print(f"Título: {self.titulo}")
        print(f"Artista: {self.artista.nombre}")
        print(f"Nacionalidad: {self.artista.nacionalidad}")
        print(f"Fecha de Nacimiento: {self.artista.nacimiento}")
        print(f"Fecha de Muerte: {self.artista.muerte}")
        print(f"Clasificación: {self.clasificacion}")
        print(f"Año de creación: {self.anio}")
        if self.url_imagen:
            print(f"URL de la imagen: {self.url_imagen}")
        else:
            print("No hay imagen disponible.")
