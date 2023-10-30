from Discos.Comandos.rmdisk import RmDisk
from Utilidades.utilidades import *
import os

def parametros_rmdisk(parametros):
    path = ""

    for parametro in parametros:

        partes = parametro.split("=")
        # SI SU LONGITUD NO ES 2 NI EMPIEZA CON EL CARACTER -, SIGUE OTRA ITERACION
        if not(len(partes) == 2 and partes[0].startswith("-")):
            continue

        parametro = partes[0][1:]  # Eliminamos el "-"
        valor = partes[1]

        match parametro.lower():
            case "path":
                valor = valor.replace('"', '')
                path = valor
            
            case _:
                return printError("El parametro -{} no existe.".format(parametro))
            
    
    # VERIFICAR QUE HAYA UN PATH
    if path == "":
        return printError("No se colocó un path.")

    # VERIFICAR QUE EL DISCO EXISTA EN LA RUTA
    if not os.path.isfile(path):
        return printError("El disco no existe en la ruta indicada.")
    
    # VERIFICAR QUE LA EXTENSION DEL DISCO SEA DSK
    if not path.endswith(".dsk"):
        return printError("Extensión de archivo no válida para la eliminación del Disco.")
            

    rm = RmDisk(path)
    return rm.remove()
