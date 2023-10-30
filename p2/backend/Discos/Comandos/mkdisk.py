from Estructuras.structs_F1 import *
from Utilidades.utilidades import *
import os
import random
import time

class MkDisk:
    def __init__(self, size, path, unit, fit):
        self._size= int(size)
        self._fit = fit
        self._unit = unit
        self._path = path

    def create(self):
        # CREA EL DISCO DURO
        size = int(self._size)

        if self._unit == "M": size *=  1024 * 1024
        if self._unit == "K": size *=  1024

        mbr_fecha_creacion = time.time()
        mbr_dsk_signature = random.randint(1, 9999)
        disco = MBR(size, mbr_fecha_creacion, mbr_dsk_signature, self._fit)

        if os.path.exists(self._path):
            return printError("Disco ya existente en la ruta: " + self._path)

        folder_path = os.path.dirname(self._path)
        os.makedirs(folder_path, exist_ok=True)

        if not self._path.endswith(".dsk"):
            return printError("Extensión de archivo no válida para la creación del Disco.")

        try:
            with open(self._path, "w+b") as file:
                file.write(b"\x00")
                file.seek(size - 1)
                file.write(b"\x00")

            # ESCRIBIMOS EL MBR
            escribir_mbr(disco, self._path)
            return printSuccess("Disco creado exitosamente!")
        except Exception:
            return printError("Error al crear el disco en la ruta: " + self._path)
