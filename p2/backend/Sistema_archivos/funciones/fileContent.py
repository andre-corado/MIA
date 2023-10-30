from Discos.Comandos.mount import ParticionesMontadas
from Estructuras.structs_F1 import *
from Estructuras.structs_F2 import *
from Utilidades.utilidades import *
from Utilidades.load import *

#FUNCION PARA OBTENER EL CONTENIDO DE UN ARCHIVO CON LA RUTA COMPLETA------------------------------------------------------------------------------
def getFileContentFromPath(id, path):
    #Se divide la ruta en carpetas
    carpetas = [elemento for elemento in path.split('/') if elemento]

    mounts = ParticionesMontadas()
    mParticion = mounts.returnPartMontada(id)
    particionEnUso:Particion = mParticion["part"]

    if mParticion is None:
        return printError("No existe la particion: {}.".format(id))
    
    # SI ES UNA PARTICION LOGICA SE SUMA EL EBR
    if particionEnUso.part_type.lower() == "l":
        temp_SB:SuperBloque = Desplazamiento_lectura_obj(mParticion["path"], particionEnUso.part_start + TAM_EBR, TAM_SB, SuperBloque())
    else:
        temp_SB:SuperBloque = Desplazamiento_lectura_obj(mParticion["path"], particionEnUso.part_start, TAM_SB, SuperBloque())
    
    # Se obtiene el inicio de inodos
    inicioInodo = temp_SB.inode_start
    inicioBlock = temp_SB.block_start

    inodo = Desplazamiento_lectura_obj(mParticion["path"], inicioInodo, TAM_INODO, Inodo())
    contenidoArch = []

    # Se recorren los bloques del nodo de inicio
    i = 0 #indice para leer cada apuntador del inodo
    j = 0 #indice para recorrer las carpetas

    while True:
        encontrado = False

        if inodo.block[i] == -1:
            break

        readfolderbloq = inodo.block[i]

        bloque = BloquesDeCarpetas()
        desplazamientoB = inicioBlock + (readfolderbloq * TAM_BLOQUE)
        list_content = Desplazamiento_lectura_obj(mParticion["path"], desplazamientoB, TAM_BLOQUE, BloquesDeCarpetas())
        bloque.b_content = list_content

        for k in range(4):
            if bloque.b_content[k].inode == -1:
                break

            name = str(bloque.b_content[k].name.strip().replace("\x00", ""))
            if name == carpetas[j]:
                # SI CONCUERDA EL NOMBRE SE OBTIENE EL INODO
                desplazamiento = inicioInodo + (bloque.b_content[k].inode * TAM_INODO)
                inodo2 = Desplazamiento_lectura_obj(mParticion["path"], desplazamiento, TAM_INODO, Inodo())

                # SE VERIFICA SI ES EL ULTIMO BLOQUE
                if j == len(carpetas) - 1:
                    for w in range(15):
                        if inodo2.block[w] == -1:
                            break

                        desplazamiento = inicioBlock + (inodo2.block[w] * TAM_BLOQUE)
                        bloqueUser = Desplazamiento_lectura_obj(mParticion["path"], desplazamiento, TAM_BLOQUE, BloquesDeArchivos())

                        contenido = str(bloqueUser.content.strip().replace("\x00", ""))
                        temp = [contenido, inodo2.block[w]]
                        contenidoArch.append(temp)   
                
                else:
                    inodo = inodo2
                    encontrado = True
                    j += 1
                    break

        if encontrado:
            i = 0
            continue

        i += 1

    return contenidoArch