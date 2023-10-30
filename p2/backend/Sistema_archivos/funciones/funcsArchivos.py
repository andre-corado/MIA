from Sistema_archivos.funciones.bloqueArchivos import get_nBloque
from Sistema_archivos.funciones.inodo import getInodeNumberForPath
from Discos.Comandos.mount import ParticionesMontadas
from Estructuras.structs_F1 import *
from Estructuras.structs_F2 import *
from Utilidades.utilidades import *
from Utilidades.load import *

#funcion para escribir en el bloque archivo n--------------------------------------------------------------------------
def modifyBlockContent(id, n, contenido):
    mounts = ParticionesMontadas()
    mParticion = mounts.returnPartMontada(id)
    particionEnUso:Particion = mParticion["part"]

    # SI ES UNA PARTICION LOGICA SE SUMA EL EBR
    if particionEnUso.part_type.lower() == "l":
        temp_SB:SuperBloque = Desplazamiento_lectura_obj(mParticion["path"], particionEnUso.part_start + TAM_EBR, TAM_SB, SuperBloque())
    else:
        temp_SB:SuperBloque = Desplazamiento_lectura_obj(mParticion["path"], particionEnUso.part_start, TAM_SB, SuperBloque())

    # SE OBTIENE EL INICIO DE BLOQUES
    inicioBloques = temp_SB.block_start

    # SE LEE EL BLOQUE
    bloque = Desplazamiento_lectura_obj(mParticion["path"], inicioBloques + (n * TAM_BLOQUE), TAM_BLOQUE, BloquesDeArchivos())
    bloque.content = contenido

    # SE ESCRIBE EL BLOQUE
    file = open(mParticion["path"], "rb+")
    Desplazamiento_escritura_obj(file, inicioBloques + (n * TAM_BLOQUE), bloque)
    file.close()

    return True

#funcion para modificar los apuntadores de un inodo---------------------------------------------------------------
def modifyFileContent(id, path, contenidocompleto):
    mounts = ParticionesMontadas()
    mParticion = mounts.returnPartMontada(id)
    particionEnUso:Particion = mParticion["part"]

    if mParticion is None:
        return printError("No existe la particion: {}.".format(id))
    
    nInodo = getInodeNumberForPath(id, path)
    
    if nInodo is None:
        return printError("Error al escribir en archivo.")
    
    # SE VERIFICA QUE YA ESTE FORMATEADA LA PARTICION A TRAVES DEL SUPER BLQOUE
    # SE CREA UN SUPER BLOQUE TEMPORAL
    temp_SB = None
    
    inicioEscritura = particionEnUso.part_start

    # SI ES UNA PARTICION LOGICA SE SUMA EL EBR
    if particionEnUso.part_type.lower() == "l":
        inicioEscritura += TAM_EBR
        temp_SB:SuperBloque = Desplazamiento_lectura_obj(mParticion["path"], particionEnUso.part_start + TAM_EBR, TAM_SB, SuperBloque())
    else:
        temp_SB:SuperBloque = Desplazamiento_lectura_obj(mParticion["path"], particionEnUso.part_start, TAM_SB, SuperBloque())

    # SE OBTIENE EL INICIO DE LOS INODOS Y BLOQUES
    inicioInodo = temp_SB.inode_start

    # SE LEE EL INODO QUE SE MANDO
    inodo = Desplazamiento_lectura_obj(mParticion["path"], inicioInodo + (nInodo * TAM_INODO), TAM_INODO, Inodo())

    #se divide el contenido en bloques de 64 caracteres
    bloques = []
    for i in range(0, len(contenidocompleto), 64):
        bloques.append(contenidocompleto[i:i+64])
    
    #se verifica que el contenido no exceda los 15 bloques del inodo
    if (len(bloques) >= 15):
        return printError("El archivo es demasiado grande")
    
    # SE RECORREN LOS BLOQUES DEL INODO
    nBloque = get_nBloque(mParticion["id"])# NUMERO DE BLOQUE QUE TOCA CREAR

    file = open(mParticion["path"], "rb+")
    
    # SE RECORREN LOS BLOQUES DEL INODO DE INICIO
    for i in range(15):

        if not(i < len(bloques)):
            break

        # SE VERIFICA QUE EL BLOQUE NO ESTE OCUPADO
        if inodo.block[i] == -1:
            # SE CREA UN NUEVO BLOQUE
            modifyBlockContent(id, nBloque, bloques[i])
            inodo.block[i] = nBloque

            #se actualiza el numero de bloques en el super bloque
            temp_SB.contCreacionBlock()

            # SE ESCIRBE EL BLOQUE EN EL BITMAP DE BLOQUES
            tam_bmInodos = calculate_n(particionEnUso.part_size)

            bitmap = Desplazamiento_lectura_normal(file, temp_SB.bmBlock_start, tam_bmInodos)

            #se modifica el bitmap
            arraybytes = list(bitmap)
            arraybytes[nBloque] = 1
            bitmap = bytes(arraybytes)
            
            #se escribe el bitmap
            Desplazamiento_escritura_normal(file, temp_SB.bmBlock_start, bitmap)
            nBloque += 1

        else:
            # SE LEE EL BLOQUE
            modifyBlockContent(id, inodo.block[i], bloques[i])

    # SE ESCRIBE EL SUPER BLOQUE
    Desplazamiento_escritura_obj(file, inicioEscritura, temp_SB)

    # SE ESCRIBE EL INODO
    Desplazamiento_escritura_obj(file, inicioInodo + (nInodo * TAM_INODO), inodo)

    file.close()

    return True