from Discos.Comandos.mount import ParticionesMontadas
from Estructuras.structs_F1 import Particion
from Utilidades.load import *

#FUNCION PARA AGREGAR BLOQUE AL BITMAP DE BLOQUES---------------------------------------------------------------------------------
def agregarBloqueEn_BM(id, n):
    particionesMount = ParticionesMontadas()

    #funcion que agrega un bloque al bitmap de bloques
    mPartition = particionesMount.returnPartMontada(id)
    particion:Particion = mPartition["part"]
    path = mPartition["path"]
    
    Temp_superB = SuperBloque()
    
    
    #Si es una particion logica se le suma el ebr
    if particion.part_type.lower() == "l":   
        Temp_superB = Desplazamiento_lectura_obj(path, particion.part_start + TAM_EBR, TAM_SB, SuperBloque())

    else:
        Temp_superB = Desplazamiento_lectura_obj(path, particion.part_start, TAM_SB, SuperBloque())
    
    inicioBitmapBloques = Temp_superB.bmBlock_start

    tam_bmInodos = calculate_n(particion.part_size)

    file = open(path, "rb+")

    bitmap = Desplazamiento_lectura_normal(file, inicioBitmapBloques, tam_bmInodos*3)
    
    #se modifica el bitmap
    arraybytes = list(bitmap)
    arraybytes[n] = 1
    bitmap = bytes(arraybytes)
    
    #se escribe el bitmap
    Desplazamiento_escritura_normal(file, inicioBitmapBloques, bitmap)
    
    #se cierra el archivo
    file.close()
    
#FUNCION PARA AGREGAR INODO AL BITMAP DE INODOS---------------------------------------------------------------------------------
def agregarInodoEn_BM(id, n):
    particionesMount = ParticionesMontadas()

    #funcion que agrega un bloque al bitmap de bloques
    mPartition = particionesMount.returnPartMontada(id)
    particion:Particion = mPartition["part"]
    path = mPartition["path"]
    
    Temp_superB = SuperBloque()
    
    
    #Si es una particion logica se le suma el ebr
    if particion.part_type.lower() == "l":   
        Temp_superB = Desplazamiento_lectura_obj(path, particion.part_start + TAM_EBR, TAM_SB, SuperBloque())

    else:
        Temp_superB = Desplazamiento_lectura_obj(path, particion.part_start, TAM_SB, SuperBloque())
    
    inicioBitmapBloques = Temp_superB.bmInode_start
    
    tam_bmInodos = calculate_n(particion.part_size)


    file = open(path, "rb+")

    bitmap = Desplazamiento_lectura_normal(file, inicioBitmapBloques, tam_bmInodos)
        
    #se modifica el bitmap
    arraybytes = list(bitmap)
    arraybytes[n] = 1
    bitmap = bytes(arraybytes)
    
    #se escribe el bitmap
    Desplazamiento_escritura_normal(file, inicioBitmapBloques, bitmap)

    #se cierra el archivo
    file.close()
