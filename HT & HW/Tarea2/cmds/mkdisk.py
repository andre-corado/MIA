import random
import datetime

# Console Line is a string splitted by spaces
def execute(consoleLine):
    # default params
    size = 0
    fit = 'FF'
    path = ''
    unit = 'M'
    # check params
    try:
        for i in range(len(consoleLine)):
            if '>size=' in consoleLine[i]:
                size = int(consoleLine[i].replace('>size=', '')) 
                if size < 1:
                    return "Error: Tamaño no válido.\n"               
                continue
            if '>fit=' in consoleLine[i]:
                fit = consoleLine[i].replace('>fit=', '').upper()
                if fit != 'BF' or fit != 'FF' or fit != 'WF':
                    return "Error: Fit no válido.\n"
                continue            
            if '>unit=' in consoleLine[i]:
                unit = consoleLine[i].replace('>unit=', '').upper()
                if unit != 'K' or unit != 'M':
                    return "Error: Unidad no válida.\n"
                continue
            if '>path=' in consoleLine[i]:
                path = consoleLine[i].replace('>path=', '')
                if path == '':
                    return "Error: Path no válido.\n"
                elif not path.endswith('.dsk'):
                    return "Error: Path no válido, debe terminar en .dsk.\n"                 
                continue       
        if unit == 'K':
            size = size * 1024
        else:
            size = size * 1024 * 1024
        mbr = MBR(size, fit)
        mbr.createDisk(path)
        return "Comando mkdisk ejecutado.\n"
    except:
        return "Error: Error en parámetros.\n"        

class MBR: # Size = 136 bytes
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
<<<<<<< Updated upstream
    # tamano-4 | fecha-19 | signature-4 | fit-1 | 
    # <-- 28 bytes --> | DATA

    # partion_1-27 | partition_2-27 | partition_3-27 | partition_4-27
    # <-- 108 bytes -->

    # TOTAL = 136 bytes

=======
    # | tamano-4 | fecha-19 | signature-4 | fit-1 | part1-27 | part2-27 | part3-27 | part4-27 |
    #   <---- SIZE = 136 BYTES ---->
    
>>>>>>> Stashed changes
    def encode(self):
        bytes = bytearray()
        bytes += self.mbr_tamano.to_bytes(4, byteorder='big')
        bytes += self.mbr_fecha_creacion.encode()
        bytes += self.mbr_dsk_signature.to_bytes(4, byteorder='big')
        bytes += self.dsk_fit.encode()
        if self.mbr_partition_1 != None:
            bytes += self.mbr_partition_1.encode()
        else:
            bytes += bytearray(27)
        if self.mbr_partition_2 != None:
            bytes += self.mbr_partition_2.encode()
        else:
            bytes += bytearray(27)
        if self.mbr_partition_3 != None:
            bytes += self.mbr_partition_3.encode()
        else:
            bytes += bytearray(27)
        if self.mbr_partition_4 != None:
            bytes += self.mbr_partition_4.encode()
        else:
            bytes += bytearray(27)
        return bytes

    def decode(self, bytes):
        self.mbr_tamano = int.from_bytes(bytes[0:4], byteorder='big')
        self.mbr_fecha_creacion = bytes[4:23].decode()
        self.mbr_dsk_signature = int.from_bytes(bytes[23:27], byteorder='big')
        self.dsk_fit = bytes[27:28].decode()
        self.mbr_partition_1 = Partition(0, '', '', 0, 0, '')
        self.mbr_partition_1.decode(bytes[28:55])
        self.mbr_partition_2 = Partition(0, '', '', 0, 0, '')
        self.mbr_partition_2.decode(bytes[55:82])
        self.mbr_partition_3 = Partition(0, '', '', 0, 0, '')
        self.mbr_partition_3.decode(bytes[82:109])
        self.mbr_partition_4 = Partition(0, '', '', 0, 0, '')
        self.mbr_partition_4.decode(bytes[109:136])

    def setFecha(self):
        # formato = d/m/Y H:M:S y quitar espacios al final
        self.mbr_fecha_creacion = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S").rstrip()


    def createDisk(self, path):
        # Crear disco en path
        with open(path, "wb") as file:
            for i in range(self.mbr_tamano):
                file.write(b'\x00')
        file.close()
        # Escribir MBR en disco
        self.setFecha()
        with open(path, "r+b") as file:
            file.write(self.encode())
        file.close()
        print("Disco creado exitosamente.")


<<<<<<< Updated upstream
class Partition: # Size = 27 bytes
    def __init__(self, status='0', type='P', fit='F', start=-1, size=0, name=''):
        self.part_status = status # Char 
        self.part_type = type # Char P o E 
        self.part_fit = fit # Char B, F o W
        self.part_start = start # Int4 signed
        self.part_s = size # Int4
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
=======
class Partition:
    def __init__(self, status, type, fit, start, size, name):
        self.part_status = status # bool 1 = activa, 0 = inactiva
        self.part_type = type # P o E
        self.part_fit = fit # F, B o W
        self.part_start = start # int 4 bytes
        self.part_size = size # int 4 bytes
        self.part_name = formatStr(name, 16) # str 16 bytes

    # ------------ STRUCTURE ------------ 
    # status-1 | type-1 | fit-1 | start-4 | size-4 | name-16 |  
    #   <---- SIZE = 27 BYTES ---->
    def encode(self):
        bytes = bytearray()
        bytes += self.part_status.to_bytes(1, byteorder='big')
        bytes += self.part_type.encode()
        bytes += self.part_fit.encode()
        bytes += self.part_start.to_bytes(4, byteorder='big')
        bytes += self.part_size.to_bytes(4, byteorder='big')
>>>>>>> Stashed changes
        bytes += self.part_name.encode()
        return bytes
    
    def decode(self, bytes):
<<<<<<< Updated upstream
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
=======
        self.part_status = int.from_bytes(bytes[0:1], byteorder='big')
        self.part_type = bytes[1:2].decode()
        self.part_fit = bytes[2:3].decode()
        self.part_start = int.from_bytes(bytes[3:7], byteorder='big')
        self.part_size = int.from_bytes(bytes[7:11], byteorder='big')
        self.part_name = bytes[11:27].decode()

    def getSizeStruct(self):
        return 1 + 1 + 1 + 4 + 4 + 16


# Limita el nombre a x caracteres, si es menor, rellena con 0
def formatStr(str, strSize):
    if len(str) > strSize:
        return str[0:strSize]
    else:
        while len(str) < strSize:
            str += '\0'
        return str
>>>>>>> Stashed changes
