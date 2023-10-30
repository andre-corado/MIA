from Reportes.generarImagen import creacionImagen
from Utilidades.utilidades import printSuccess
from Estructuras.structs_F1 import *

def reporteDISK(pathMBR, pathImagen):
    mbr = obtener_mbr(pathMBR)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CODIGO DOT <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    dot = 'digraph G {\n\n'

    dot += 'node [fontname="Helvetica,Arial,sans-serif"]\n'
    dot += 'edge [fontname="Helvetica,Arial,sans-serif"]\n'

    # DEFINICION DE TABLA
    dot += 'node [shape=plaintext];\n\n'
    dot += '\ttabla [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4">\n'

    # ENCABEZADO
    dot += '\t\t<tr rowspan="2">\n'

    # MBR
    dot += '\t\t\t<td rowspan="2"><b>MBR</b></td>\n'

    # VARIABLES 
    lista_ebr = []
    colspan, size_disk_ocupado, size_extended, cant_no_activas = 0, 0, 0, 0
    porcentaje_ext = 0

    # SE OBTIENE LA SUMA TOTAL DEL DISCO
    for particion in mbr.mbr_Partitions:
        if particion.part_status == "0":
            cant_no_activas += 1
            continue

        size_disk_ocupado += int(particion.part_size)

    # TAM DISPONIBLE
    size_disk_disp = mbr.mbr_tamano - size_disk_ocupado

    # TAMAÑO QUE DEBE DE OCUPAR CADA PARTICION QUE NO ESTA ACTIVA
    cantidad_repartir_noActivas = 0
    if cant_no_activas != 0:
        cantidad_repartir_noActivas = size_disk_disp / cant_no_activas

    # SE RECORRE LAS PARTICIONES PARA BUSCAR UNA EXTENDIDA Y OBTENER EL COLSPAN
    for particion in mbr.mbr_Partitions:

        tam_particion = particion.part_size

        if particion.part_status == "0": tam_particion = cantidad_repartir_noActivas

        # CALCULO DE PORCENTAJES
        porcentaje = (tam_particion / mbr.mbr_tamano) * 100  # PORCENTAJE QUE OCUPA LA PARTICION EN DISCO
        porcentaje_format = "{:.2f}".format(porcentaje)            # MUESTRA CON 2 DECIMALES

        if particion.part_type.lower() == "e" and particion.part_status == "1":

            lista_ebr = obtener_ebrList(pathMBR, particion.part_start)
            colspan = (len(lista_ebr) * 2) + 1
            porcentaje_ext = float(porcentaje_format)

            # SI SE ENCUENTRA CON UNA PARTICION EXTENDIDA, SE OBTIENE EL TAMAÑO
            size_extended = int(particion.part_size)

            # EXTENDIDA
            dot += '\t\t\t<td colspan="'+ str(colspan) +'"><b>Extendida</b>  <b>' + str(porcentaje_format) + '%</b></td>\n'
            continue
        
        # VERIFICAMOS SI ES UNA PARTICION AÑADIDA Y SU TIPO ES PRIMARIA
        if particion.part_type.lower() == "p" and particion.part_status == "1":
            dot += '\t\t\t<td rowspan="2"><b>Primaria</b>  <b>' + str(porcentaje_format) + '%</b></td>\n'

        # VERIFICAMOS SI NO ESTAN ACTIVAS, O SEA NO TIENEN DATOS
        if particion.part_status == "e":
            dot += '\t\t\t<td rowspan="2"><b>nil</b>  <b>' + str(porcentaje_format) + '%</b></td>\n'

    if size_disk_disp > 0 and cant_no_activas == 0:
        porcentaje = (size_disk_disp / mbr.mbr_tamano) * 100  # PORCENTAJE QUE OCUPA LA PARTICION EN DISCO
        porcentaje_format = "{:.2f}".format(porcentaje)       # MUESTRA CON 2 DECIMALES
        dot += '\t\t\t<td rowspan="2"><b>nil</b>  <b>' + str(porcentaje_format) + '%</b></td>\n'

    elif size_disk_disp > 0:
        porcentaje = (size_disk_disp / mbr.mbr_tamano) * 100  # PORCENTAJE QUE OCUPA LA PARTICION EN DISCO
        porcentaje_format = "{:.2f}".format(porcentaje)       # MUESTRA CON 2 DECIMALES
        dot += '\t\t\t<td rowspan="2"><b>nil</b>  <b>' + str(porcentaje_format) + '%</b></td>\n'

    # FIN ENCABEZADOS
    dot += '\t\t</tr>\n'

    # SE AGREGA LOS EBR Y PARTICIONES LOGICAS
    if len(lista_ebr) != 0:

        # OBTENGO EL TAMAÑO QUE TODOS LOS EBR OCUPAN
        size_ocupado = sum(ebr.part_size for ebr in lista_ebr)
        contador_ebrs = 0

        dot += '\t\t<tr>\n'

        for i in range(len(lista_ebr)):
            ebr:EBR = lista_ebr[i]

            porcentaje = (ebr.part_size / size_extended) * porcentaje_ext  # PORCENTAJE QUE OCUPA LA PARTICION EN DISCO
            porcentaje_format = "{:.2f}".format(porcentaje)     # MUESTRA CON 2 DECIMALES

            if ebr.part_status == "e":
                contador_ebrs += 1
                dot += '\t\t\t<td><b>nil</b>  <b>' + str(porcentaje_format) + '%</b></td>\n'
                continue

            # SE AGREGA
            dot += '\t\t\t<td><b>EBR</b></td>\n'
            dot += '\t\t\t<td><b>Logica</b>  <b>'+ str(porcentaje_format) +'%</b></td>\n'
            contador_ebrs += 1

        # ESPACIO LIBRE DE LA PARTICION EXTENDIDA
        espacio_disp = size_extended - size_ocupado - (31 * contador_ebrs)
        
        if espacio_disp > 0:
            porcentaje = (espacio_disp / size_extended) * porcentaje_ext  # PORCENTAJE QUE OCUPA LA PARTICION EN DISCO
            porcentaje_format = "{:.2f}".format(porcentaje)                # MUESTRA CON 2 DECIMALES

            dot += '\t\t\t<td><b>nil</b>  <b>' + str(porcentaje_format) + '%</b></td>\n'

       # FIN EBR Y LOGICAS
        dot += '\t\t</tr>\n'

    # Cerrar la definición de la tabla
    dot += '\t</table>>];\n'

    # Cerrar el digraph
    dot += '\n}'


    # CREACION DE IMAGEN Y ASIGNACION DE RUTA
    creacionImagen(pathImagen, dot)

    return printSuccess("Rep DISK ha sido generado exitosamente")
