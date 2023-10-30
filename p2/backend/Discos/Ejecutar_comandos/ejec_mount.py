
from Discos.Comandos.mount import ParticionesMontadas
from Estructuras.structs_F1 import *
from Utilidades.utilidades import *
import os

def parametros_mount(parametros):
    path, name = "", ""

    for elemento in parametros:

        partes = elemento.split("=")
        # SI SU LONGITUD NO ES 2 NI EMPIEZA CON EL CARACTER -, SIGUE OTRA ITERACION
        if not(len(partes) == 2 and partes[0].startswith("-")):
            continue

        parametro = partes[0][1:]  # Eliminamos el "-"
        valor = partes[1]

        match parametro.lower():
            case "path":
                valor = valor.replace('"', '')
                path = valor

            case "name":
                entrada_sin_comillas = valor.replace('"', '')
                name = entrada_sin_comillas

            case _:
                return f"El parametro -{parametro} no existe."


    #       <<<<<<<<<<<<<<<<<<<< VALIDACIONES >>>>>>>>>>>>>>>>>>>>

    # VERIFICAR SI EL DISCO EXISTE
    if not os.path.exists(path):
        return printError("Disco no existente en la ruta: {}".format(path))

    # VERIFICAR LA EXTENSION
    if not path.endswith(".dsk"):
        return printError("Extensión de archivo no válida para la creación del Disco.")
    
    # VERIFICAR SI EXISTE LA PARTICION
    num_particion, particion = buscarParticionPL(path, name)

    if num_particion is None:
        return printError("No se encontró la partición {}.".format(name))

    # OBTENGO EL NOMBRE DEL DISCO
    nombre_disk = os.path.splitext(os.path.basename(path))[0]

    # DETERMINAR EL ID DE LA PARTICION A MONTAR
    ult_dosDigitos_carnet = 18 # 202103718
    idFinal = str(ult_dosDigitos_carnet) + str(num_particion) + nombre_disk
    particionesMount = ParticionesMontadas()
    particionesMount.agregarParticion(idFinal, path, particion)
    print(printConsola("Id de la particion montada: {}".format(idFinal)))
    print("\n")
    return printSuccess("MOUNT: La partición {} fue montada correctamente!".format(name))


def buscarParticionPL(path, id):
    mbr = obtener_mbr(path)

    for indiceP, particion in enumerate(mbr.mbr_Partitions):
        name = str(particion.part_name.strip().replace("\x00", ""))
        if name == id and particion.part_type.lower() != "e" and particion.part_status == "1":
            return indiceP, particion

        if particion.part_type.lower() == "e":
            listEBR = obtener_ebrList(path, particion.part_start)

            for indiceL, logic in enumerate(listEBR):
                name = str(logic.part_name.strip().replace("\x00", ""))
                if name == id and logic.part_status == "1":
                    return indiceL, logic

    return None, None        
