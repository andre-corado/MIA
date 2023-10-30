from Discos.Comandos.mkdisk import MkDisk
from Utilidades.utilidades import *

def comandos_mkdisk(parametros):
    size, path, unit, fit = "", "", "", ""

    for elemento in parametros:

        partes = elemento.split("=")
        # SI SU LONGITUD NO ES 2 NI EMPIEZA CON EL CARACTER -, SIGUE OTRA ITERACION
        if not(len(partes) == 2 and partes[0].startswith("-")):
            continue

        parametro = partes[0][1:]  # Eliminamos el "-"
        valor = partes[1]

        match parametro.lower():
            case "size":
                size = valor

            case "path":
                valor = valor.replace('"', '')
                path = valor

            case "unit":
                unit = valor.upper()

            case "fit":
                fit = valor.upper()
                
            case _:
                return printError("El parametro -{} no existe.".format(parametro))

    # VALORES POR DEFECTO A LOS PARAMETROS OPCIONALES
    if unit == "": unit = "M"
    if fit == "": fit = "FF"

    # VERIFICA  QUE EL VALOR DE SIZE SEA UN NUMERO
    if not(size.isdigit()):
        return printError("El valor -size={} debe ser un valor númerico entero.".format(size))
    
    # VERIFICAR QUE EL VALOR DE SIZE SEA MAYOR A 0 Y POSITIVO
    if int(size) <= 0:
        return printError("El parámetro size del comando MKDISK debe ser mayor a 0")
    
    # VERIFICA QUE LOS VALORES SEAN BF, FF O WF
    if not fit in ["BF", "FF", "WF"]:
        return printError("El valor -fit={} no pertenece a los valores válidos".format(fit))
    
    # VERIFICA QUE LOS VALORES SEAN K O M
    if not unit in ["K", "M"]:
        return printError("El valor -unit={} no pertenece a los valores válidos.".format(unit))
    
    # LUEGO DE RECOLECTAR LOS PARAMETROS CREA EL DISCO DURO
    disk = MkDisk(size, path, unit, fit)
    return disk.create()