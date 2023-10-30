class SesionActiva:
    _instancia = None
    _sesion_iniciada = None  # USER QUE LA INICIO
    _sesion_Particion = ""   # ID DE LA PARTICION
    _path_Particion = ""     # PATH DE LA PARTICION

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(SesionActiva, cls).__new__(cls)

        return cls._instancia

    # Métodos para acceder y modificar la variable global y el nuevo atributo
    def getSesion_iniciada(self):
        return self._sesion_iniciada

    def SetSesion_iniciada(self, valor):
        self._sesion_iniciada = valor

    def getSesion_Particion(self):
        return self._sesion_Particion

    def SetSesion_Particion(self, sesion):
        self._sesion_Particion = sesion

    def getPath_Particion(self):
        return self._path_Particion

    def SetPath_Particion(self, path):
        self._path_Particion = path
