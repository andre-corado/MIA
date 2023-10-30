from Sistema_archivos.funciones.fileContent import getFileContentFromPath
from Utilidades.utilidades import printSuccess
import os
import svgwrite

def reporteFILE(particionMount, pathImagen, rutaR_File):
    nombre_archivo, _ = os.path.splitext(os.path.basename(pathImagen))

    vecArch = getFileContentFromPath(particionMount["id"], rutaR_File)
    titulo = "RUTA: \"" + rutaR_File + "\""

    pathSVG = f"./Reportes/Reportes_svg/{nombre_archivo}.svg"
    dwg = svgwrite.Drawing(filename=pathSVG, profile='tiny', size=('800px', '5200px'))

    # POSICION
    x = 300
    y = 90

    dwg.add(dwg.text(titulo, insert=(str(310), str(y)), font_size='20'))
    y += 35
    
    for i in range(len(vecArch)):
        dwg.add(dwg.text(vecArch[i][0], insert=(str(x), str(y)), font_size='17'))
        y += 22

    dwg.save()

    return printSuccess("Rep FILE ha sido generado exitosamente")