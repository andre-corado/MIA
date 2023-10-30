from Discos.Comandos.mount import ParticionesMontadas
from Estructuras.structs_F2 import *
from Utilidades.utilidades import *
from Utilidades.load import *

def obtenerInfoInodo_1(path:str, inodo:Inodo, seekBlock:int):
    cadena = ""

    for apt in inodo.block:
        if apt == -1:
            # SIGNIFICA QUE NO HAY NINGUN BLOQUE EN EL APUNTADOR
            break

        # SI HAY UN BLOQUE EN EL APUNTADOR
        bloque = Desplazamiento_lectura_obj(path, seekBlock, TAM_BLOQUE, BloquesDeArchivos())
        seekBlock += TAM_BLOQUE

        # VOY JUNTANDO TODO EL CONTENIDO DE CADA BLQOEU
        cadena += str(bloque.content.strip().replace("\x00", ""))
        
    return cadena


# - MODIFICAR APUNTADORES DE INODO
# - CREAR LOS DEMAS BLOQUES
def escribirInfoInodo_1(path:str, inodo:Inodo, seekBlock:int, cadenaEntrada:str, seeks, superB:SuperBloque):

    # ALMACENA EN UN ARREGLO i CANTIDAD DE CADENAS CON TAMAÑO 64 BYTES
    distro_bloques = _dividir_cadena(cadenaEntrada)

    for indice, apt in enumerate(inodo.block):
        file = open(path, "rb+")

        if apt != -1: 
            nuevoBlockArchivos_existe = BloquesDeArchivos(distro_bloques.pop(0))
            Desplazamiento_escritura_obj(file, seekBlock, nuevoBlockArchivos_existe)
            seekBlock += TAM_BLOQUE
            continue

        if len(distro_bloques) == 0: break

        # SE CAMBIA EL ESTADO DEL APUNTADOR
        numBloque = _numBloqueArch(path, seeks, superB)
        inodo.block[indice] = numBloque
 
        # SE CREAN Y ESCRIBEN LOS BLOQUES DE ARCHIVOS
        superB.blocks_count += 1
        
        nuevoBlockArchivos = BloquesDeArchivos(distro_bloques.pop(0))
        Desplazamiento_escritura_obj(file, seekBlock, nuevoBlockArchivos)
        seekBlock += TAM_BLOQUE

        file.close()


def _dividir_cadena(cadena, longitud=64):
    subcadenas = []
    indice_inicio = 0

    while indice_inicio < len(cadena):
        subcadena = cadena[indice_inicio:indice_inicio+longitud]
        subcadenas.append(subcadena)
        indice_inicio += longitud

    return subcadenas

def _numBloqueArch(path, seeks, superB:SuperBloque):
    seekStartBmBlock = seeks[0]
    part_size = seeks[1]

    file = open(path, "rb+")

    # OBTENGO MI BIT MAP 
    tam_bmInodos = calculate_n(part_size)
    tam_bmBlocks = tam_bmInodos * 3

    bitmapBlocks = Desplazamiento_lectura_normal(file, seekStartBmBlock, tam_bmBlocks)

    # RECORRER EL BITMAP CONTANDO TODOS LOS 1's
    contador = 0
    for i in range(len(bitmapBlocks)):
        if (bitmapBlocks[i] != 1):
            break
        contador += 1

    # RELLENO DE BLOQUE USADO EN EL BITMAP
    desplazamiento = seekStartBmBlock + contador
    Desplazamiento_escritura_normal(file, desplazamiento, b"\1")

    file.close()


    return contador

# ////////////////////////////////////////////////////////////////////////////////////////////////

def escribirInfoInodo_0(path:str, inodo:Inodo, seekBlock:int, cadenaEntrada:str):

    # ALMACENA EN UN ARREGLO i CANTIDAD DE CADENAS CON TAMAÑO 64 BYTES
    distro_bloques = _dividir_cadena(cadenaEntrada)

    for apt in inodo.block:
        
        if apt == -1: break
        if len(distro_bloques) == 0: break

        file = open(path, "rb+")

        nuevoBlockArchivos = BloquesDeArchivos(distro_bloques.pop(0))
        Desplazamiento_escritura_obj(file, seekBlock, nuevoBlockArchivos)
        seekBlock += TAM_BLOQUE

        file.close()


#FUNCION PARA OBTENER EL NUMERO DE INODO ACTUAL-------------------------------------------------------------------------
def get_nInodo(id):
    particionesMount = ParticionesMontadas()

    #funcion que recorre el bitmap de inodos, cuenta los 1s y devuelve el numero que toca
    mPartition = particionesMount.returnPartMontada(id)
    particion:Particion = mPartition["part"]
    path = mPartition["path"]
    
    Temp_superB = SuperBloque()
    
    #Si es una particion logica se le suma el ebr
    if particion.part_type.lower() == "l":
        Temp_superB:SuperBloque = Desplazamiento_lectura_obj(path, particion.part_start + TAM_EBR, TAM_SB, SuperBloque())
    else:
        Temp_superB:SuperBloque = Desplazamiento_lectura_obj(path, particion.part_start, TAM_SB, SuperBloque())
    
    inicioBitmapInodos = Temp_superB.bmInode_start


    Crrfile = open(path, 'rb+')

    # OBTENGO MI BIT MAP 
    tam_bmInodos = calculate_n(particion.part_size)
    
    #se lee el bitmap de bloques
    bitmap = Desplazamiento_lectura_normal(Crrfile, inicioBitmapInodos, tam_bmInodos)
        
    #se recorre el bitmap y se cuentan los 1s
    contador = 0
    for i in range(len(bitmap)):
        if (bitmap[i] != 1):
            break
        contador += 1
    #se cierra el archivo
    Crrfile.close()
    
    return contador


#FUNCION PARA OBTENER EL BLOQUE ACTUAL--------------------------------------------------------------------------------------------
def get_nBloque(id):
    particionesMount = ParticionesMontadas()

    #funcion que recorre el bitmap de inodos, cuenta los 1s y devuelve el numero que toca
    mPartition = particionesMount.returnPartMontada(id)
    particion:Particion = mPartition["part"]
    path = mPartition["path"]
    
    Temp_superB = SuperBloque()
    
    
    #Si es una particion logica se le suma el ebr
    if particion.part_type.lower() == "l":
        Temp_superB:SuperBloque = Desplazamiento_lectura_obj(path, particion.part_start + TAM_EBR, TAM_SB, SuperBloque())
    else:
        Temp_superB:SuperBloque = Desplazamiento_lectura_obj(path, particion.part_start, TAM_SB, SuperBloque())
    
    inicioBitmapBloques = Temp_superB.bmBlock_start


    Crrfile = open(path, 'rb+')

    # OBTENGO MI BIT MAP 
    tam_bmInodos = calculate_n(particion.part_size)
    tam_bmBlocks = tam_bmInodos * 3
    
    #se lee el bitmap de bloques
    bitmap = Desplazamiento_lectura_normal(Crrfile, inicioBitmapBloques, tam_bmBlocks)
        
    #se recorre el bitmap y se cuentan los 1s
    contador = 0
    for i in range(len(bitmap)):
        if (bitmap[i] != 1):
            break
        contador += 1
    #se cierra el archivo
    Crrfile.close()
    
    return contador