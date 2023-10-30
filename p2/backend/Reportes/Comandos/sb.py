from Reportes.generarImagen import creacionImagen
from Utilidades.utilidades import printSuccess
from Estructuras.structs_F2 import *
from Estructuras.structs_F1 import *
from Utilidades.load import *
import os


TAM_SUPERB = 80

def reporteSB(particionMount, pathImagen):
    path = particionMount["path"]
    nombreDisk, extDisk = os.path.splitext(os.path.basename(particionMount["path"]))

    particion:Particion = particionMount["part"]
    posicion_SB = particion.part_start
    
    superBloque = Desplazamiento_lectura_obj(path, posicion_SB, TAM_SUPERB, SuperBloque())

    codigo_dot = "digraph H{\n"
    codigo_dot += "\tgraph [pad=\"0.5\", nodesep=\"0.5\", ranksep=\"1\"];\n"
    codigo_dot += "\tnode [shape=plaintext]\n"
    codigo_dot += "\trankdir=LR;\n"

    codigo_dot += "\tSuperBloque [\n"
    codigo_dot += "\t\tlabel=<\n"
    codigo_dot += "\t\t\t<table border=\"0\" cellborder=\"1\" cellspacing=\"0\">\n"
    codigo_dot += "\t\t\t\t<tr><td colspan=\"3\" port='0'>SuperBloque</td></tr>\n"

    codigo_dot += f"<tr><td>nombre_hd</td><td port='1'>{str(nombreDisk+extDisk)}</td></tr>\n"
    codigo_dot += superBloque.graphvizBS()

    codigo_dot += "\t\t</table>\n"
    codigo_dot += "\t>];\n"
    codigo_dot += "}\n"

    # CREACION DE IMAGEN Y ASIGNACION DE RUTA
    creacionImagen(pathImagen, codigo_dot)

    return printSuccess("Rep SUPER BLOQUE ha sido generado exitosamente")