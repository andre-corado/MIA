import random
import datetime
import struct


def execute(consoleLine):
    # Analizador de parámetros futuros

    mbr = MBR()
    mbr.createDisk()
    return "Comando mkdisk ejecutado.\n"


class MBR:
    def __init__(self):
        self.format = "H19sH"

        self.mbr_tamano = 5
        self.mbr_fecha_creacion = ""
        self.mbr_dsk_signature = random.randint(111, 65535)

    def encode(self):
        return struct.pack(self.format, self.mbr_tamano, self.mbr_fecha_creacion.encode(), self.mbr_dsk_signature)

    def decode(self, data):
        return struct.unpack(self.format, data)

    def setFecha(self):
        # formato = d/m/Y H:M:S y quitar espacios al final
        self.mbr_fecha_creacion = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S").rstrip()


    def createDisk(self):
        with open("mbr.dsk", "wb") as file:
            for i in range(0, self.mbr_tamano):
                file.write(b'\x00' * 1024 * 1024)
        file.close()
        self.setFecha()
        with open("mbr.dsk", "r+b") as file:
            file.write(self.encode())
        file.close()
        print("Disco creado exitosamente.")


class Decode:
    pass