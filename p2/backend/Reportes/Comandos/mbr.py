from Reportes.generarImagen import creacionImagen
from Utilidades.utilidades import printSuccess
from Estructuras.structs_F1 import *
import datetime

def reporteMBR(pathImagen, pathMBR):
    mbr = obtener_mbr(pathMBR)

    # COLOR MBR Y PARTICIONES
    bgcolor_mbr ="purple:violet"
    color_cuerpo_mbr = "#AE9EFA"
    

    codigo_dot = "digraph G{\n"
    codigo_dot += "\trankdir=TB;\n"
    codigo_dot += "\tnode [shape=plaintext];\n"

    codigo_dot += "\ttabla [label=<\n"
    codigo_dot += "\t\t<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\">\n"

    # :>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MBR <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    codigo_dot += f"\t\t\t<TR><TD colspan=\"2\">REPORTE DE MBR</TD></TR>\n"

    # COLOCAR DATOS DEL MBR
    codigo_dot += f"\t\t\t<TR><TD>Tamano</TD><TD>{str(mbr.mbr_tamano)}</TD></TR>\n"
    fecha = datetime.datetime.fromtimestamp(mbr.mbr_fecha_creacion).strftime('%Y-%m-%d %H:%M:%S')
    codigo_dot += f"\t\t\t<TR><TD>Fecha_creacion</TD><TD>{str(fecha)}</TD></TR>\n"
    codigo_dot += f"\t\t\t<TR><TD>Disk_signature</TD><TD>{str(mbr.mbr_dsk_signature)}</TD></TR>\n"


    # :>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PARTICIONES Y LOGICAS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    for particion in mbr.mbr_Partitions:
        codigo_dot += f"\t\t\t<TR><TD colspan=\"2\">Particion</TD></TR>\n"
        codigo_dot += f"\t\t\t<TR><TD>Status</TD><TD>{str(particion.part_status)}</TD></TR>\n"
        codigo_dot += f"\t\t\t<TR><TD>Type</TD><TD>{str(particion.part_type)}</TD></TR>\n"

        fit = str(particion.part_fit.strip().replace("\x00", ""))
        codigo_dot += f"\t\t\t<TR><TD>Fit</TD><TD>{str(fit)}</TD></TR>\n"
        codigo_dot += "\t\t\t<TR><TD>Start</TD><TD>{}</TD></TR>\n".format(color_cuerpo_mbr, str(particion.part_start))
        codigo_dot += f"\t\t\t<TR><TD>Size</TD><TD>{str(particion.part_size)}</TD></TR>\n"

        particion_name = str(particion.part_name.strip().replace("\x00", ""))
        codigo_dot += f"\t\t\t<TR><TD>Name</TD><TD>{str(particion_name)}</TD></TR>\n"
        #
        # EN CASO EXISTA UNA EXTENDIDA DEBE DE IMPRIMIRSE TODAS LAS PARTICIONES LOGICAS
        if particion.part_type.lower() == "e":
            ebr = obtener_ebr(pathMBR, particion.part_start)
            codigo_dot += ebr.graphvizEBR(pathMBR)
       
    codigo_dot += "\t\t</TABLE>\n"
    codigo_dot += "\t>];\n"
    codigo_dot += "}\n"


    # CREACION DE IMAGEN Y ASIGNACION DE RUTA
    creacionImagen(pathImagen, codigo_dot)

    return printSuccess("Rep MBR ha sido generado exitosamente.")
