import random
import datetime


def execute(consoleLine):
    # Analizador de parámetros futuros

    mbr = MBR()
    mbr.createDisk()
    return "Comando mkdisk ejecutado.\n"


class MBR:
    def __init__(self, size, fit='F'):
        self.mbr_tamano = size
        self.mbr_fecha_creacion = ""
        self.mbr_dsk_signature = random.randint(0, 2147483646)
        self.dsk_fit = fit
        self.mbr_partition_1 = None
        self.mbr_partition_2 = None
        self.mbr_partition_3 = None
        self.mbr_partition_4 = None
    
    # ------------ STRUCTURE ------------
    # tamano-4 | fecha-19 | signature-4 | fit-1 
    
    def encode(self):
        bytes = bytearray()
        bytes += self.mbr_tamano.to_bytes(4, byteorder='big')
        bytes += self.mbr_fecha_creacion.encode()
        bytes += self.mbr_dsk_signature.to_bytes(4, byteorder='big')
        bytes += self.dsk_fit.encode()
        return bytes

    def decode(self, bytes):
        self.mbr_tamano = int.from_bytes(bytes[0:4], byteorder='big')
        self.mbr_fecha_creacion = bytes[4:23].decode()
        self.mbr_dsk_signature = int.from_bytes(bytes[23:27], byteorder='big')
        self.dsk_fit = bytes[27:28].decode() 

    def setFecha(self):
        # formato = d/m/Y H:M:S y quitar espacios al final
        self.mbr_fecha_creacion = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S").rstrip()


    def createDisk(self):
        with open("mbr.dsk", "wb") as file:
            for i in range(self.mbr_tamano):
                file.write(b'\x00')
        file.close()
        self.setFecha()
        with open("mbr.dsk", "r+b") as file:
            file.write(self.encode())
        file.close()
        print("Disco creado exitosamente.")
