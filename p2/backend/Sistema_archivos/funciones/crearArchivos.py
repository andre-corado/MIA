from Sistema_archivos.funciones.funcsArchivos import modifyFileContent
from Sistema_archivos.funciones.inodo import getInodeNumberForPath
from Sistema_archivos.funciones.bloqueArchivos import *
from Discos.Comandos.mount import ParticionesMontadas
from Sistema_archivos.funciones.bitmaps import *
from Estructuras.structs_F1 import *
from Estructuras.structs_F2 import *
from Utilidades.utilidades import *
from Utilidades.load import *
import random
import time

def crearArchivo(id, path, size, cont):
    mounts = ParticionesMontadas()
    mParticion = mounts.returnPartMontada(id)
    particionEnUso:Particion = mParticion["part"]

    # OBTENGO LA FECHA.
    date = time.time()

    if mParticion is None:
        return printError("No existe la particion: {}.".format(id))
    
    nInodo = getInodeNumberForPath(id, path)
    
    if nInodo is not None:
        return printError("Ya existe un archivo con ese nombre.")
    
    #Se obtiene la ruta completa hasta la carpeta padre
    carpetas = [elemento for elemento in path.split('/') if elemento]
    carpeta_a_crear = carpetas.pop()

    pathCarpetaPadre = ''

    for carpeta in carpetas:
        pathCarpetaPadre = pathCarpetaPadre + '/' + carpeta
        
    #Se obtiene el numero del inodo de la carpeta padre
    if (pathCarpetaPadre == ''):
        nInodoPadre = 0
    else:
        nInodoPadre = getInodeNumberForPath(id, pathCarpetaPadre)

    if nInodoPadre is None:
        return printError("No existe la carpeta padre.")
    
    contenidofinal = ""

    # SE VERIFICA SI LA VARIABLE CONT ES VACIO
    if cont != "":
        # SE LEE EL CONTENIDO DE LA RUTA DEL ARCHIVO EN LA COMPUTADORA
        try:
            archivo = open(cont, 'r')
            contenidofinal = archivo.read()
            archivo.close()

        except Exception as e:
            return printError("No existe el archivo.")

    elif size != 0:
        #Se llena el contenido con numeros del 0 al 9 random
        for i in range(int(size)):
            contenidofinal = contenidofinal + str(random.randint(0, 9))

    else:
        return printError("Falta el parametro size o cont")
    
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
    inicioBlock = temp_SB.block_start

    # SE LEE EL INODO QUE SE MANDO
    inodoPadre = Desplazamiento_lectura_obj(mParticion["path"], inicioInodo + (nInodoPadre * TAM_INODO), TAM_INODO, Inodo())

    # SE BUSCA ENTRE SUS APUNTADORES DE BLOQUES SI EXISTE UN ESPACIO
    nInodo = get_nInodo(mParticion["id"])# NUMERO DE INODO QUE TOCA CREAR
    nBloque = get_nBloque(mParticion["id"])# NUMERO DE BLOQUE QUE TOCA CREAR

    # SE RECORREN LOS BLOQUES DEL INODO DE INICIO
    for i, apuntador in enumerate(inodoPadre.block):

        if apuntador != -1:

            # SE LEE EL BLOQUE
            bloqueCarpetas = BloquesDeCarpetas()
            desplazamientoB = inicioBlock + (apuntador * TAM_BLOQUE)
            list_content = Desplazamiento_lectura_obj(mParticion["path"], desplazamientoB, TAM_BLOQUE, BloquesDeCarpetas())
            bloqueCarpetas.b_content = list_content

            # SE RECORRE EL BLOQUE
            for j, bloque in enumerate(list_content):
                if not (bloque.inode == -1):
                    continue

                # SE MODIFICA EL BLOQUE ACTUAL CON EL NUEVO INODO
                bloqueCarpetas.b_content[j].inode = nInodo
                bloqueCarpetas.b_content[j].name = carpeta_a_crear

                # SE ESCRIBE EL BLOQUE
                file = open(mParticion["path"], "rb+")

                Desplazamiento_escritura_obj(file, inicioBlock + (apuntador * TAM_BLOQUE), bloqueCarpetas)

                # SE CREA EL NUEVO INODO QUE REPRESENTA A LA CARPETA
                inodo = Inodo(nInodo, nInodo, 0, date, date, date, [-1]*15, "1", 664)
                inodo.block[0] = nBloque

                # SE ESCRIBE EL INODO NUEVO
                Desplazamiento_escritura_obj(file, inicioInodo + (nInodo * TAM_INODO), inodo)

                # SE CREA UN NUEVO BLOQUE DE ARCHIVOS VACIO
                bloque = BloquesDeArchivos()

                # SE ESCRIBE EL BLOQUE NUEVO
                Desplazamiento_escritura_obj(file, inicioBlock + (nBloque * TAM_BLOQUE), bloque)

                # SE ACTUALIZA EL NUMERO DE INODOS EN EL SUPERBLOQUE
                agregarBloqueEn_BM(mParticion["id"], nBloque)
                agregarInodoEn_BM(mParticion["id"], nInodo)

                # ACTTUALIZA LOS CONTADORES DE CANTIDAD USADA Y CANTIDAD DISPONIBLE
                temp_SB.contCreacionInodo()
                temp_SB.contCreacionBlock()

                # SE ESCRIBE EL SUPER BLOQUE
                Desplazamiento_escritura_obj(file, inicioEscritura, temp_SB)

                file.close()

                # SE MODIFICA EL CONTENIDO DEL BLOQUE
                if modifyFileContent(id, path, contenidofinal):              
                    return True
                
                return False
            
        # SI NO EXISTE UN ESPACIO SE CREA UN NUEVO BLOQUE
        else:
            inodoPadre.block[i] = nBloque

            file = open(mParticion["path"], "rb+")

            # SE ESCRIBE EL INODO PADRE
            Desplazamiento_escritura_obj(file, inicioInodo + (nInodoPadre * TAM_INODO), inodoPadre)

            # SE CREA EL NUEVO BLOQUE VACIO
            bloque = BloquesDeCarpetas()

            # SE LLENA EL CONTENIDO DE 0
            bloque.b_content[0].inode = nInodo
            bloque.b_content[0].name = carpeta_a_crear

            # SE ESCRIBE EL BLOQUE NUEVO
            Desplazamiento_escritura_obj(file, inicioBlock + (nBloque * TAM_BLOQUE), bloque)

            #SE CREA EL NUEVO INODO QUE REPRESENTA A LA CARPETA
            inodo = Inodo(nInodo, nInodo, 0, date, date, date, [-1]*15, "1", 664)
            inodo.block[0] = nBloque

            # SE ESCRIBE EL INODO
            Desplazamiento_escritura_obj(file, inicioInodo + (nInodo * TAM_INODO), inodo)

            # SE CREA UN NUEVO BLOQUE DE ARCHIVOS VACIO
            bloque = BloquesDeArchivos()

            # SE ESCRIBE EL BLOQUE NUEVO
            Desplazamiento_escritura_obj(file, inicioBlock + (nBloque * TAM_BLOQUE), bloque)

            # SE ACTUALIZA EL NUMERO DE INODOS EN EL SUPERBLOQUE
            agregarBloqueEn_BM(mParticion["id"], nBloque)
            agregarInodoEn_BM(mParticion["id"], nInodo)

            # ACTTUALIZA LOS CONTADORES DE CANTIDAD USADA Y CANTIDAD DISPONIBLE
            temp_SB.contCreacionInodo()
            temp_SB.contCreacionBlock()

            # SE ESCRIBE EL SUPER BLOQUE
            Desplazamiento_escritura_obj(file, inicioEscritura, temp_SB)

            file.close()

            # SE MODIFICA EL CONTENIDO DEL BLOQUE
            if modifyFileContent(id, path, contenidofinal):              
                return True
            
            return False    
    
    return False