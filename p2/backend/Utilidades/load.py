import math
from Estructuras.structs_F1 import *
from Estructuras.structs_F2 import *
from Utilidades.utilidades import *


def Desplazamiento_escritura_normal(archivo, desplazamiento, texto):
    archivo.seek(desplazamiento)
    archivo.write(texto)

def Desplazamiento_lectura_normal(archivo, desplazamiento, size):
    try:
        archivo.seek(desplazamiento)
        data = archivo.read(size)
        return data
    except Exception as e:
        print(f"Error:{e} while reading in: ", desplazamiento)
        pass

def Desplazamiento_escritura_obj(archivo, desplazamiento, obj):
    data = obj.serealizar()
    
    archivo.seek(desplazamiento)
    archivo.write(data)

def Desplazamiento_lectura_obj(path, desplazamiento, tamanio, obj):
    with open(path, "rb+") as file:
        file.seek(desplazamiento)
        data = file.read(tamanio)
        return obj.deserealizar(data)

# BUSQUEDA DE INODO POR NOMBRE
def buscarInodo(particionMount, nombreInodo):
    path = particionMount["path"]
    particion:Particion = particionMount["part"]
    posicion_SB = particion.part_start

    superBloque = Desplazamiento_lectura_obj(path, posicion_SB, TAM_SB, SuperBloque())

    # SE OBTIENE LA POSICION INICIAL DEL INODO RAIZ
    posInodeStart = superBloque.inode_start
    posBlockStart = superBloque.block_start
    inodo:Inodo() = Desplazamiento_lectura_obj(path, posInodeStart, TAM_INODO, Inodo())

    return _recorrerInodo(nombreInodo, path, inodo, posInodeStart, posBlockStart)    

def _recorrerInodo(nombreInodo:str, path:str, inodo:Inodo, seekInodo:int, seekBloque:str):
    seekInodo += TAM_INODO

    for apt in inodo.block:
        if apt == -1: continue

        if inodo.type_ == "0":
            obj_carpetas:BloquesDeCarpetas = Desplazamiento_lectura_obj(path, seekBloque, TAM_BLOQUE, BloquesDeCarpetas())
            seekBloque += TAM_BLOQUE

            for carpeta in obj_carpetas:
                name = str(carpeta.name.strip().replace("\x00", ""))
                if name == "." or name == ".." or carpeta.inode == -1:
                    continue

                inodo = Desplazamiento_lectura_obj(path, seekInodo, TAM_INODO, Inodo())
                if name == nombreInodo: return inodo, seekBloque
                
                i, bloqueSeek =_recorrerInodo(nombreInodo, path, inodo, seekInodo, seekBloque)
                if i is not None:
                    return i
                
                seekInodo += TAM_INODO

# Funcion para calcular el numero de inodos (n)
def calculate_n(size: int):
    # Numerador         = (mounted_partition.size - sizeof(Superblock)
    numerator = size - TAM_SB

    # Denominador_Base  = (4 + sizeof(Inode) + 3 * sizeof(Fileblock))
    base_denominator = 4 + TAM_INODO + 3 * TAM_BLOQUE

    # n                 = floor(numerador / denominador)
    n = math.floor(numerator / base_denominator)

    return n
