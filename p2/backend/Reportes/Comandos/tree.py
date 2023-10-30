from Discos.Comandos.mount import ParticionesMontadas
from Estructuras.structs_F2 import *
from Reportes.generarImagen import generate_dot
from Utilidades.load import *
from Utilidades.utilidades import *
import os

def reporteBloquesHijos(bloque, path, Temb_suberB:SuperBloque, n):    
    reporte = ""

    if hasattr(bloque, 'content'):
        reporte += bloque.generar_reporte_archivos(n)

    else:
        aux = bloque 
        bloque = BloquesDeCarpetas()
        bloque.b_content = aux

        reporte += bloque.generarBloqueRep(n)
        for k in range(4):
            if(bloque.b_content[k].inode == -1):
                continue

            name = str(bloque.b_content[k].name.strip().replace("\x00", ""))
            if(name == '.' or name == '..'):
                continue

            inodo = Desplazamiento_lectura_obj(path, Temb_suberB.inode_start + bloque.b_content[k].inode * TAM_INODO, TAM_INODO, Inodo())
            reporte += reporteInodoHijos(inodo, path, Temb_suberB)
            reporte += "Bloque" + str(n) + ":" +str(k+1) + " -> " + "Inodo" + str(bloque.b_content[k].inode) +":0;" + " "
        
    return reporte


def reporteInodoHijos(inodo:Inodo, path, Temp_suberB:SuperBloque):
    reporte = ""

    reporte += inodo.generarInodoRep()

    i = 0

    while True:
        if inodo.block[i] == -1:
            break

        readfolderbloq = inodo.block[i]

        if(inodo.type_ == "0"):
            bloquefold:BloquesDeCarpetas = Desplazamiento_lectura_obj(path, Temp_suberB.block_start + (readfolderbloq * TAM_BLOQUE), TAM_BLOQUE, BloquesDeCarpetas())
            reporte += reporteBloquesHijos(bloquefold, path, Temp_suberB, inodo.block[i])
        else:
            bloquearch:BloquesDeArchivos = Desplazamiento_lectura_obj(path, Temp_suberB.block_start + (readfolderbloq * TAM_BLOQUE), TAM_BLOQUE, BloquesDeArchivos())
            reporte += reporteBloquesHijos(bloquearch, path, Temp_suberB, inodo.block[i])

        reporte += "Inodo" + str(inodo.uid) + ":" +str(i+1) + " -> " + "Bloque" + str(inodo.block[i])+":0;" + " "
        i += 1

    return reporte


def reporteTree(idParticion):
    mPartition = ParticionesMontadas().returnPartMontada(idParticion)

    if mPartition["part"].part_type.lower() == "l":
        Temp_suberB:SuperBloque = Desplazamiento_lectura_obj(mPartition["path"], mPartition["part"].part_start + TAM_EBR, TAM_SB, SuperBloque())
    else:
        Temp_suberB:SuperBloque = Desplazamiento_lectura_obj(mPartition["path"], mPartition["part"].part_start, TAM_SB, SuperBloque())

    reporte = ""

    inicioInodo = Temp_suberB.inode_start

    inodoinicial:Inodo = Desplazamiento_lectura_obj(mPartition["path"], inicioInodo, TAM_INODO, Inodo())

    reporte += reporteInodoHijos(inodoinicial, mPartition["path"], Temp_suberB)

    return reporte


def reporteTREE(particionMount, pathImagen):
    reporte = "digraph G{ graph [pad=\"0.5\", nodesep=\"0.5\", ranksep=\"1\"];node [shape=plaintext] rankdir=LR;"
    reporte += reporteTree(particionMount["id"])
    reporte += "}"

    nombre_archivo, extension = os.path.splitext(os.path.basename(pathImagen))

    return generate_dot(reporte, pathImagen, nombre_archivo)
