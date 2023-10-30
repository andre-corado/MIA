class ParticionesMontadas:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ParticionesMontadas, cls).__new__(cls)
            cls._instancia.particiones_montadas = []
        
        return cls._instancia

    def agregarParticion(self, id, path, particion):
        self.particiones_montadas.append({"id": id, "path": path, "part": particion})

    def obtenerParticiones(self):
        return self.particiones_montadas

    def returnPartMontada(self, id):
        for part in self.particiones_montadas:
            if part["id"] == id:
                return part
            
        return None

    def buscarParticion(self, id):
        for particion in self.particiones_montadas:
            if particion["id"] == id:
                return True
            
        return False
