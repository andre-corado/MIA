from Discos.Comandos.mount import ParticionesMontadas
from Estructuras.structs_F2 import SuperBloque
from Utilidades.load import *

def buscarInodo_path_EXT(pathEXT, superB:SuperBloque, path):
    carpetas = [elemento for elemento in pathEXT.split('/') if elemento]
    
    inodo0 = Desplazamiento_lectura_obj(path, superB.inode_start, TAM_INODO, Inodo())

    return __buscarInodoPorPathEXT(carpetas, inodo0, superB, path)


def __buscarInodoPorPathEXT(listPath, inodo:Inodo, superB:SuperBloque, path):
    index = 0
    buscarNombre = listPath.pop(0)

    for i in inodo.block:
        if not i != -1:
            index += 1
            continue

        if index < 13:

            # DETECTA  LA CARPETA
            desplazamiento = superB.block_start + (i * TAM_BLOQUE)
            blockCarpetas = Desplazamiento_lectura_obj(path, desplazamiento, TAM_BLOQUE, BloquesDeCarpetas())

            # RECORRE LAS CARPETAS DENTRO DEL BLOQUE DE CARPETAS
            for contenido in blockCarpetas:
                if not contenido.inode != -1:
                    continue

                if str(contenido.name.strip().replace("\x00", "")) == buscarNombre:
                    if len(listPath) == 0:
                        return contenido.inode
                    
                    else:
                        desplazamiento = superB.inode_start + (contenido.inode * TAM_INODO)
                        sigInodo = Desplazamiento_lectura_obj(path, desplazamiento, TAM_INODO, Inodo())
                        return __buscarInodoPorPathEXT(listPath, sigInodo, superB, path)

        index += 1


def getInodeNumberForPath(id, pathEXT):
    # Se divide la ruta en carpetas
    carpetas = [elemento for elemento in pathEXT.split("/") if elemento]

    # SE BUSCA LA PARTICION
    particionMount = ParticionesMontadas()

    mParticion = particionMount.returnPartMontada(id)
    particion:Particion = mParticion["part"]

    if mParticion is None:
        return printError("No existe la particion")

    # SE VERIFICA QUE YA ESTE FORMATEADA LA PARTICION A TRAVES DEL SUPER BLOQUE
    temp_sb = SuperBloque()

    if particion.part_type.lower() == "l":
        temp_sb:SuperBloque = Desplazamiento_lectura_obj(mParticion["path"], particion.part_start + TAM_EBR, TAM_SB, SuperBloque())
    else:
        temp_sb:SuperBloque = Desplazamiento_lectura_obj(mParticion["path"], particion.part_start, TAM_SB, SuperBloque())

    # SE OBTIENE EL INICIO DE INODOS
    inicioInodos = temp_sb.inode_start
    inicioBLocks = temp_sb.block_start

    inodo:Inodo = Desplazamiento_lectura_obj(mParticion["path"], inicioInodos, TAM_INODO, Inodo())

    i = 0 # indice para leer cada apuntador del inodo
    j = 0 # indice para recorrer las carpetas

    while True:
        encontrado = False

        if inodo.block[i] == -1:
            break

        leer_carpetaBloque = inodo.block[i]

        # SE LEE EL BLOQUE
        bloque = BloquesDeCarpetas()
        bloque_content = Desplazamiento_lectura_obj(mParticion["path"], inicioBLocks + (leer_carpetaBloque * TAM_BLOQUE), TAM_BLOQUE, BloquesDeCarpetas())
        bloque.b_content = bloque_content

        # SE RECORRE EL BLOQUE
        for k in range(4):
            if bloque.b_content[k].inode == -1:
                break

            nameBlock = str(bloque.b_content[k].name.strip().replace("\x00", ""))
            if nameBlock == carpetas[j]:
                inodo2 = Desplazamiento_lectura_obj(mParticion["path"], inicioInodos + (bloque.b_content[k].inode * TAM_INODO), TAM_INODO, Inodo())

                if j == len(carpetas) - 1:
                    return bloque.b_content[k].inode
                
                else: 
                    inodo = inodo2
                    encontrado = True
                    j += 1
                    break
        
        if encontrado is True:
            i = 0
            continue
        i += 1

    return None







