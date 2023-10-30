import struct

class Particion:# 28 Bytes en total
    def __init__(self, status = "0", type_ = "P", fit = "_", start = -1, size = -1, name = ""): 
        self.part_status = status # 1 Bytes          
        self.part_type = type_    # 1 Bytes          
        self.part_fit = fit       # 2 Bytes      
        self.part_start = start   # 4 Bytes  
        self.part_size = size     # 4 Bytes
        self.part_name = name     # 16 Bytes

    def serealizar(self):
        part_status_pack = struct.pack("1s", self.part_status.encode())
        part_type_pack = struct.pack("1s", self.part_type.encode())
        part_fit_pack = struct.pack("2s", self.part_fit.encode())
        part_start_pack = struct.pack("i", self.part_start)
        part_size_pack = struct.pack("i", self.part_size)
        part_name_pack = struct.pack("16s", self.part_name.encode())

        total_pack = part_status_pack + part_type_pack + part_fit_pack + part_start_pack + part_size_pack + part_name_pack
        return total_pack
    
    @classmethod
    def deserializar(cls, data):
        part_status = struct.unpack("1s", data[:1])[0].decode()
        part_type = struct.unpack("1s", data[1:2])[0].decode()
        part_fit = struct.unpack("2s", data[2:4])[0].decode()
        part_start = struct.unpack("i", data[4:8])[0]
        part_size = struct.unpack("i", data[8:12])[0]
        part_name = struct.unpack("16s", data[12:28])[0].decode("utf-8").strip()

        return cls(part_status, part_type, part_fit, part_start, part_size, part_name)



from typing import List

class MBR:# 130 bytes en total
    def __init__(self, mbr_tamano: int, mbr_fecha_creacion: float, mbr_dsk_signature: int, dsk_fit: str):
        self.mbr_tamano = mbr_tamano                    #  4 Bytes
        self.mbr_fecha_creacion = mbr_fecha_creacion    #  8 Bytes
        self.mbr_dsk_signature = mbr_dsk_signature      #  4 Bytes
        self.dsk_fit = dsk_fit                          #  2 Bytes => 18 Bytes
        self.mbr_Partitions: List[Particion] = []       # 4 * 28 Bytes
        self._definirParticiones()

    def _definirParticiones(self):
        for _ in range(4):
            self.mbr_Partitions.append(Particion())

    def añadir_particion(self, particion: Particion, i: int):
        self.mbr_Partitions[i] = particion
    
    def returnParticionExt(self):
        for particion in self.mbr_Partitions:
            if particion.part_type.lower() == "e":
                return particion
            
    
    def espacioDisponibleEnMBR(self, nuevoEspacio):
        espacioOcupado = 0

        for particion in self.mbr_Partitions:
            if particion.part_size != -1 and particion.part_status.lower() != "e":
                espacioOcupado += particion.part_size

        tamDIsk = self.mbr_tamano - 130#MBR
        espacioDisponible =  tamDIsk - espacioOcupado
        print("Espacio a ocupar: {}".format(str(nuevoEspacio)))
        print("ESPACIO DISPONIBLE EN EL DISCO {}\n".format(str(espacioDisponible)))
        if nuevoEspacio < espacioDisponible:
            return False
        
        return True

    def serealizar(self):
        mbr_tamano_pack = struct.pack("i", self.mbr_tamano)
        mbr_fecha_creacion_pack = struct.pack("d", self.mbr_fecha_creacion)
        mbr_dsk_signature_pack = struct.pack("i", self.mbr_dsk_signature)
        dsk_fit_pack = struct.pack("2s", self.dsk_fit.encode())

        # Particiones
        partitions_pack = b""
        for particion in self.mbr_Partitions:
            partitions_pack += particion.serealizar()

        return (mbr_tamano_pack + mbr_fecha_creacion_pack +
                mbr_dsk_signature_pack + dsk_fit_pack +
                partitions_pack)
    
    @classmethod
    def deserealizar(cls, data):
        mbr_tamano = struct.unpack("i", data[:4])[0]
        mbr_fecha_creacion = struct.unpack("d", data[4:12])[0]
        mbr_dsk_signature = struct.unpack("i", data[12:16])[0]
        dsk_fit = struct.unpack("2s", data[16:18])[0].decode("utf-8")

        mbr_tam_info = 18
        mbr_tam_particion = 28
        particiones = []

        for i in range(mbr_tam_info, len(data), mbr_tam_particion):
            particion = Particion.deserializar(data[i:i + mbr_tam_particion])
            particiones.append(particion)

        # Creamos el disco 
        mbr_disco = cls(mbr_tamano, mbr_fecha_creacion, mbr_dsk_signature, dsk_fit)
        mbr_disco.mbr_Partitions = particiones

        return mbr_disco
    
# Escribimos el MBR en el archivo especificado
def escribir_mbr(data:MBR, path):
    pack_data = data.serealizar()

    with open(path, "rb+") as file:
        file.seek(0)
        file.write(pack_data)

# Obtenemos el MBR del archivo especificado
def obtener_mbr(path: str):
    try:
        with open(path, "rb+") as file:
            data = file.read(130)
            return MBR.deserealizar(data)
    
    except Exception as e:
        print(e)
        print("Ocurrio un error al obtener el mbr")

class EBR:# 31 Bytes en total
    def __init__(self, status = "0", fit = "_", start = -1, size = -1, next_ = -1, name = ""):
        self.part_status = status #  1 Bytes
        self.part_fit = fit       #  2 Bytes
        self.part_start = start   #  4 Bytes
        self.part_size = size     #  4 Bytes
        self.part_next = next_    #  4 Bytes
        self.part_name = name     # 16 Bytes

    def printEBRS(self, path):
        current:EBR = obtener_ebr(path, self.part_start)
        n = 1
        while True:
            if current.part_next != -1:
                print("----- PARTICION LOGICA {} -----".format(str(n)))
                print("status: {}, fit: {}\start: {}, size: {}\nnext: {}, name: {}".format(current.part_status, current.part_fit, str(current.part_start), str(current.part_size), str(current.part_next), current.part_name))
                print("-------------------------------")
            else:
                break
            
            n += 1
            start = current.part_next
            current = obtener_ebr(path, start)

    def tam_disp_extendida(self, path):
        current:EBR = obtener_ebr(path, self.part_start)
        sizeFinal = 0

        while True:
            if current.part_size == -1:
                return sizeFinal

            sizeFinal += current.part_size + 31
            
            start = current.part_next
            if start == -1:
                return sizeFinal

            current = obtener_ebr(path, start)

    def verificarNombreRepetido(self, path, nombre):
        current:EBR = obtener_ebr(path, self.part_start)

        while True:
            print("\n")
            nombreCurrent = str(current.part_name.strip().replace("\x00", ""))
            if nombreCurrent == nombre:
                return True
            
            start = current.part_next
            if start == -1:
                return False

            current = obtener_ebr(path, start)

    def graphvizEBR(self, path):
        current:EBR = obtener_ebr(path, self.part_start)
        cadena = ""

        while True:
            cadena += f"\t\t\t<TR><TD colspan=\"2\">Particion Logica</TD></TR>\n"

            cadena += f"\t\t\t<TR><TD>status</TD><TD>{str(current.part_status)}</TD></TR>\n"
            cadena += f"\t\t\t<TR><TD>next</TD><TD>{str(current.part_next)}</TD></TR>\n"
            fit = str(current.part_fit.strip().replace("\x00", ""))
            cadena += f"\t\t\t<TR><TD>fit</TD><TD>{str(fit)}</TD></TR>\n"
            cadena += f"\t\t\t<TR><TD>start</TD><TD>{str(current.part_start)}</TD></TR>\n"
            cadena += f"\t\t\t<TR><TD>size</TD><TD>{str(current.part_size)}</TD></TR>\n"
            particion_name = str(current.part_name.strip().replace("\x00", ""))
            cadena += f"\t\t\t<TR><TD>name</TD><TD>{str(particion_name)}</TD></TR>\n"

            start = current.part_next
            if start == -1:
                return cadena

            current = obtener_ebr(path, start)
    
    def serealizar(self):    
        status = struct.pack("1s", self.part_status.encode()) 
        fit = struct.pack("2s", self.part_fit.encode())    
        start = struct.pack("i", self.part_start)            
        size = struct.pack("i", self.part_size)             
        next_ = struct.pack("i", self.part_next)             
        name = struct.pack("16s", self.part_name.encode())

        pack = status + fit + start + size + next_ + name
        return pack

    @classmethod
    def deserealizar(cls, data):
        status = struct.unpack("1s", data[:1])[0].decode("utf-8")  
        fit = struct.unpack("2s", data[1:3])[0].decode("utf-8") 
        start = struct.unpack("i", data[3:7])[0]           
        size = struct.unpack("i", data[7:11])[0]          
        next_ = struct.unpack("i", data[11:15])[0]
        name = struct.unpack("16s", data[15:31])[0].decode("utf-8").strip()

        return cls(status, fit, start, size, next_, name)
    

def escribir_ebr(obj: EBR, path:str, start:int):
    pack_data = obj.serealizar()

    with open(path, "rb+") as file:
        file.seek(start)
        file.write(pack_data)

# Obtenemos el EBR del archivo especificado
def obtener_ebr(path: str, start:int):

    with open(path, "rb+") as file:
        file.seek(start)
        data = file.read(31)
        return EBR.deserealizar(data)
        

def obtener_ebrList(path: str, start: int):

    ebr_list = []
    current_start = start

    with open(path, "rb+") as file:
        while True:

            file.seek(current_start)
            data = file.read(31)
            if not data:
                break
            ebr = EBR.deserealizar(data)
            ebr_list.append(ebr)

            # Actualizar la posición actual al siguiente EBR
            current_start = ebr.part_next

            if current_start == -1:
                break
            
    return ebr_list
