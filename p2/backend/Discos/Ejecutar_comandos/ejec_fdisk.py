from Discos.Comandos.fdisk import FDisk
from Estructuras.structs_F1 import *
from Utilidades.utilidades import *
import os

def existeParticion_PL(path, name):
    mbr = obtener_mbr(path)

    for particion in mbr.mbr_Partitions:
        nameParticion = str(particion.part_name.strip().replace("\x00", ""))

        if nameParticion == name and particion.part_type.lower() != "e":
            return True
        
        if particion.part_type.lower() == "e":
            listEBR = obtener_ebrList(path, particion.part_start)

            for logic in listEBR:
                if str(logic.part_name.strip().replace("\x00", "")) == name:
                    return True
                
            if nameParticion == name:
                return True
            
    return False


def parametros_fdisk(parametros):
    size, path, name, tipo, unit = "", "", "", "", 0

    for elemento in parametros:
        
        partes = elemento.split("=")
        # SI SU LONGITUD NO ES 2 NI EMPIEZA CON EL CARACTER -, SIGUE OTRA ITERACION
        if not(len(partes) == 2 and partes[0].startswith("-")):
            continue

        parametro = partes[0][1:]  # Eliminamos el "-"
        valor = partes[1]

        match parametro.lower():
            case "size":
                size = int(valor)

            case "path":
                valor = valor.replace('"', '')
                path = valor

            case "name":
                entrada_sin_comillas = valor.replace('"', '')
                name = entrada_sin_comillas

            case "type":
                tipo = valor.upper()

            case "unit":

                if valor.lower() not in ["k", "m", "b"]:
                    return printError("Revise el -unit")

                if valor.lower() == "k":
                    unit = 1024

                elif valor.lower() == "m":
                    unit = 1024 * 1024
                    
            case _:
                return printError(f"El parametro -{parametro} no existe.")


    if tipo == "": tipo = "P"
    if unit == 0: unit = 1024

    #       <<<<<<<<<<<<<<<<<<<< VALIDACIONES >>>>>>>>>>>>>>>>>>>>

    # Obtenemos el mbr del disco
    MBR_:MBR = obtener_mbr(path)

    # VERIFICAR QUE EL DISCO EXISTA
    if not os.path.isfile(path): return printError("El disco no existe.")
    
    # VERIFICAR SI EXISTE LA PARTICION 
    existeParticion = existeParticion_PL(path, name)

    # VERIFICAR QUE EL TAMAÑO QUE SE COLOCO SEA MAYOR A 0
    if size <= 0:
        return printError("Verifique el size de la particion")

    size *= unit

    # VERIFICAR QUE NO EXISTE UNA PARTICION DEL MISMO NOMBRE
    if existeParticion is True: return printError("Ya existe una partición con el mismo nombre.")
        
    # VERIFICAR EL TAMAÑO DE LA PARTICION -> NEWPARTICION < TAMAÑO_DISCO
    if size > MBR_.mbr_tamano - 130: return printError("El tamaño de la particion es mayor al tamaño del disco")
    
    # VERIFICAR QUE EL TYPE SEA ALGUNAS DE LAS DISPONIBLES(P,E,L)
    if tipo not in ["P", "E", "L"]: return printError("El tipo -type={} no existe".format(tipo))


    # EN CASO SEA LOGICA, VERIFICAR >>>>>>>>>>>>>>>>
    if tipo.lower() == "l":
        # VERIFICAR QUE EXISTA UN PARTICION EXTENDIDA
        existeExtendida = any(particion.part_type.lower() == 'e' for particion in MBR_.mbr_Partitions)

        if existeExtendida is False:
            return printError("Para crear particiones lógicas, debe de existir una particion extendida.")

        # VERIFICAR QUE LA PARTICION A INGRESAR, QUEPA EN LA PARTICION EXTENDIDA
        p_extendida:Particion = MBR_.returnParticionExt()
        ebr_inicial = obtener_ebr(path, p_extendida.part_start)
        total_ocupado = ebr_inicial.tam_disp_extendida(path)

        espacioDisp = p_extendida.part_size - total_ocupado
        print("TAMAÑO_DISPONIBLE_EXT: {}".format(espacioDisp))
        if size + 31 > espacioDisp:
            return printError("No hay espacio suficiente para la particion {}".format(name))
        
        # VERIFICAR QUE NO SE REPITA EL NOMBRE
        if ebr_inicial.verificarNombreRepetido(path, name):
            return printError("Ya existe una particion con el nombre: {}".format(name))
        

    # VERIFICA SI EL ESPACIO DE LA NUEVA PARTICION, CABE EN EL DISCO
    if MBR_.espacioDisponibleEnMBR(size) and tipo.lower() != "l":
        return printError("No hay espacio suficiente en el disco para la particion {}".format(name))
    
    # VERIFICAR QUE EN LAS 4 PARTICIONES SOLO EXISTA UNA EXTENDIDA
    for particion in MBR_.mbr_Partitions:
        if tipo.lower() == "e" and particion.part_type.lower() == 'e':
            return printError("Ya existe una particion extendida.")
    
    
    # LUEGO DE RECOLECTAR LOS PARAMETROS CREA EL DISCO DURO
    particion = FDisk(size, path, name, tipo)
    return particion.crear_particion(MBR_)
