import os
import random
import datetime


class MBR:  # Size = 136 bytes
    def __init__(self, fit, size):
        self.mbr_tamano = size
        self.mbr_fecha_creacion = ""
        self.mbr_dsk_signature = random.randint(0, 2147483646)
        self.dsk_fit = fit
        self.mbr_partition_1 = None
        self.mbr_partition_2 = None
        self.mbr_partition_3 = None
        self.mbr_partition_4 = None

    # ------------ STRUCTURE ------------
    # tamano-4 | fecha-19 | signature-4 | fit-1 | 
    # <-- 28 bytes --> | DATA

    # partion_1-27 | partition_2-27 | partition_3-27 | partition_4-27
    # <-- 108 bytes -->

    # TOTAL = 136 bytes

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

    def createDisk(self, path):
        print('Creando disco en :' + path + '...')
        if path.startswith('\"'):
           path = path[1:-1]
           if os.path.exists(os.path.dirname(path)) == False:
               # Crear directorio
                os.makedirs(os.path.dirname(path))
        else:
            if os.path.exists(os.path.dirname(path)) == False:
                # Crear directorio
                os.makedirs(os.path.dirname(path))
        with open(path, "wb") as file:
            for i in range(self.mbr_tamano):
                file.write(b'\x00')
        file.close()
        self.setFecha()
        with open(path, "r+b") as file:
            file.write(self.encode())
        file.close()
        print("Disco creado exitosamente.")


class Partition:  # Size = 27 bytes
    def __init__(self, status='0', type='P', fit='F', start=-1, size=0, name=''):
        self.part_status = status  # Char
        self.part_type = type  # Char P o E
        self.part_fit = fit  # Char B, F o W
        self.part_start = start  # Int4 signed
        self.part_s = size  # Int4
        self.part_name = formatStr(name, 16)

    # ------------ STRUCTURE ------------
    # status-1 | type-1 | fit-1 | start-4 | size-4 | name-16
    # <-- 27 bytes -->

    def encode(self):
        bytes = bytearray()
        bytes += self.part_status.encode()
        bytes += self.part_type.encode()
        bytes += self.part_fit.encode()
        bytes += self.part_start.to_bytes(4, byteorder='big', signed=True)
        bytes += self.part_s.to_bytes(4, byteorder='big')
        bytes += self.part_name.encode()
        return bytes

    def decode(self, bytes):
        self.part_status = bytes[0:1].decode()
        self.part_type = bytes[1:2].decode()
        self.part_fit = bytes[2:3].decode()
        self.part_start = int.from_bytes(bytes[3:7], byteorder='big', signed=True)
        self.part_s = int.from_bytes(bytes[7:11], byteorder='big')
        self.part_name = bytes[11:27].decode()


def formatStr(string, size):
    if len(string) < size:
        string += (size - len(string)) * '\x00'
    elif len(string) > size:
        string = string[:size]
    return string
