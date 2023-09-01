import os
import random
import datetime
import graphviz as gv

class MBR:  # Size = 136 bytes
    def __init__(self, fit='F', size=0):
        self.mbr_tamano = size
        self.mbr_fecha_creacion = ""
        self.mbr_dsk_signature = random.randint(0, 2147483646)
        self.dsk_fit = fit
        self.mbr_partition_1 = Partition()
        self.mbr_partition_2 = Partition()
        self.mbr_partition_3 = Partition()
        self.mbr_partition_4 = Partition()

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
        bytes += self.mbr_partition_1.encode()
        bytes += self.mbr_partition_2.encode()
        bytes += self.mbr_partition_3.encode()
        bytes += self.mbr_partition_4.encode()
        return bytes

    def decode(self, bytes):
        self.mbr_tamano = int.from_bytes(bytes[0:4], byteorder='big')
        self.mbr_fecha_creacion = bytes[4:23].decode()
        self.mbr_dsk_signature = int.from_bytes(bytes[23:27], byteorder='big')
        self.dsk_fit = bytes[27:28].decode()
        self.mbr_partition_1.decode(bytes[28:55])
        self.mbr_partition_2.decode(bytes[55:82])
        self.mbr_partition_3.decode(bytes[82:109])
        self.mbr_partition_4.decode(bytes[109:136])

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

    def getPartitions(self):
        return [self.mbr_partition_1, self.mbr_partition_2, self.mbr_partition_3, self.mbr_partition_4]

    def getPartitionIndexForFF(self, size):
        for i in range(4):
            partition = self.getPartitions()[i]
            if partition.part_status == 'N' and partition.part_s >= size:
                return i
        return -1
    
    def getNewPartitionStart(self, indexPartition):
        if indexPartition == 0:
            return 137
        else:
            return self.getPartitions()[indexPartition - 1].part_start + self.getPartitions()[indexPartition - 1].part_s

# VALIDACIONES

    def hasExtendedPartition(self):
        for partition in self.getPartitions():
            if partition.part_type == 'E':
                return True
        return False
    
    def hasFreePrimaryPartition(self):
        for partition in self.getPartitions():
            if partition.part_status == 'N':
                return True
        return False

    def hasPartitionNamed(self, name):
        for partition in self.getPartitions():
            if partition.part_name == formatStr(name, 16):
                return True
        return False

    def canAddPartition(self, size):
        for partition in self.getPartitions():
            if partition.part_status == 'N' and partition.part_s >= size:
                return True
        return False
        

    # Graphviz
    def getGraph(self):
        # Encabezado MBR
        dot = gv.Digraph()

        with dot.subgraph(name='encabezadoMBR') as b1:
            b1.attr(label='MBR')
            b1.node('Title', 'MBR', shape='plaintext', fontsize='20')
            b1.node_attr.update(shape='box', style='filled', fillcolor='lightgray', width='2', height='1')
            txt = 'Tamaño: ' + str(self.mbr_tamano) + '\n' + 'Fecha Creación: ' + self.mbr_fecha_creacion + '\n'
            txt += 'Signature: ' + str(self.mbr_dsk_signature) + '\n' + 'Fit: ' + self.dsk_fit
            b1.node('B1', label=txt)
            b1.edge('Title', 'B1', style='invis')



        with dot.subgraph(name='part0') as part0:
            part0.node('Title', 'Partición Primaria', shape='plaintext', fontsize='20')
            part0.node_attr.update(shape='box', style='filled', fillcolor='lightgray', width='2', height='1')
            txt = 'Status: ' + self.mbr_partition_1.part_status + '\n' + 'Tipo: ' + self.mbr_partition_1.part_type + '\n'
            txt += 'Fit: ' + self.mbr_partition_1.part_fit + '\n' + 'Start: ' + str(self.mbr_partition_1.part_start) + '\n'
            txt += 'Size: ' + str(self.mbr_partition_1.part_s) + '\n' + 'Name: '
            part0.node('B2', label=txt)

        dot.edge('B1', 'B2', style='invis')
        dot.attr(rank='same', B1='', B2='')
        dot.attr(ranksep='0.1')

        '''# Obtener subgrafos de particiones
        for i in range(len(self.getPartitions())):
            partition = self.getPartitions()[i]
            nameSubGraph = 'partition' + str(i)
            if partition.part_type == 'P':
                with dot.subgraph(name=nameSubGraph) as b:
                    b.attr(label='Partición Primaria', rankdir='TB', style='filled', color='lightgrey', shape='box')
                    b.node('Title', 'Partición Primaria', shape='plaintext', fontsize='20')
                    txt = 'Status: ' + partition.part_status + '\n' + 'Tipo: ' + partition.part_type + '\n'
                    txt += 'Fit: ' + partition.part_fit + '\n' + 'Start: ' + str(partition.part_start) + '\n'
                    txt += 'Size: ' + str(partition.part_s) + '\n' + 'Name: ' + partition.part_name
                    b.node('Info', label=txt, shape='box')
                    dot.edge('Title', 'Info', style='invis')
            elif partition.part_type == 'E':
                return 'Error: No se puede graficar partición extendida.'

            if i == 0:
                dot.edge('Info', 'partition0', style='invis')
            else:
                dot.edge('partition' + str(i - 1), 'partition' + str(i), style='invis')'''

        return dot







class Partition:  # Size = 27 bytes
    def __init__(self, status='N', type='P', fit='F', start=-1, size=0, name='asd'):
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
        self.part_name = bytes[11:27].decode().replace('\x00', '')





def formatStr(string, size):
    if len(string) < size:
        string += (size - len(string)) * '\x00'
    elif len(string) > size:
        string = string[:size]
    return string

