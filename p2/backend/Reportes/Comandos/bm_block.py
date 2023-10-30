from Reportes.Comandos.bm_inode import _dividir_cadena_bm
from Utilidades.utilidades import printSuccess
from Estructuras.structs_F1 import *
from Utilidades.load import *
import svgwrite
import os

TAM_SB = 80

def reporteBM_BLOCK(particionMount, pathSVG):
    path = particionMount["path"]
    nombre_archivo, _ = os.path.splitext(os.path.basename(pathSVG))

    # OBTENER LA PARTICION QUE SE ESTA USANDO Y EL SUPERBLOQUE
    particionEnUso: Particion = particionMount["part"]
    superB = Desplazamiento_lectura_obj(path, particionEnUso.part_start, TAM_SB, SuperBloque())

    # SE OBTIENE EL TAMAÑO DEL BITMAP DE BLOCK
    tam_bmInodos = calculate_n(particionEnUso.part_size)
    tam_bmBlocks = tam_bmInodos * 3

    # SE OBTIENE DATOS DEL BITMAP POR MEDIO DEL RANGO 
    file = open(path, "rb+")
    bitmap = Desplazamiento_lectura_normal(file, superB.bmBlock_start, tam_bmBlocks)
    file.close()

    # EL CONTENIDO DEL BITMAP SE CONVIERTE A CADENA
    cadena = ''.join(map(str, bitmap))

    # HACE LAS SEPARACIONES DE 20 BYTES POR LÍNEA
    arreglo = _dividir_cadena_bm(cadena)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>. CREACION DE ARCHIVO SVG <<<<<<<<<<<<<<<<<<<<<<<<<<<

    # CREACIÓN DEL ARCHIVO SVG
    pathSVG = f"./Reportes/Reportes_svg/{nombre_archivo}.svg"
    dwg = svgwrite.Drawing(filename=pathSVG, profile='tiny', size=('4000px', '12500px'))

    y = 30  # Coordenada Y inicial
    x = 50
    flag = False
    flag2 = False
    flag3 = False
    flag4 = False

    for elemento in arreglo:
        cadena_con_espacios = '  '.join(elemento)

        if y > len(arreglo)*3 and flag is False:
            flag = True
            y = 30
            x = 880

        elif y > len(arreglo)*3 and flag2 is False:
            flag2 = True
            y = 30
            x = 1600
        
        elif y > len(arreglo)*3 and flag3 is False:
            flag3 = True
            y = 30
            x = 2400
        
        elif y > len(arreglo)*3 and flag4 is False:
            flag4 = True
            y = 30
            x = 3200

        dwg.add(dwg.text(cadena_con_espacios, insert=(str(x), str(y)), font_size='11'))
        y += 10  # Ajusta la posición Y para la siguiente línea

    dwg.save()

    return printSuccess("Rep BM_BLOCK ha sido generado exitosamente")

