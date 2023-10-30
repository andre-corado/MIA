from Utilidades.utilidades import *
import os

class RmDisk:
    def __init__(self, path_):
        self._path = path_

    def remove(self):
        try:       
            os.remove(self._path)
            return printSuccess("Disco eliminado correctamente!")

        except Exception:
            return printError("Error al intentar eliminar el disco.")
