from General.Importaciones import *

def leerComando(consola):

    if consola.lower() == "mparticiones":
        # Creamos una instancia de la clase ListMountedPartitions
        particiones_montadas = ParticionesMontadas()
        parts = ""

        # Obtenemos las particiones montadas
        particiones = particiones_montadas.obtenerParticiones()

        if len(particiones) == 0:
            return printError("No existen particiones montadas.")
        else:
            parts += "\t<<<Ejecutado>>> Particiones montadas.\n\n"

        # Imprimimos las particiones
        for i, particion in enumerate(particiones):
            parts += " {}) Id: {}, path: {}\n".format(str(i+1), particion["id"], particion["path"])

        parts += "\n<-------------------------------------->"

        return parts

    # Utilizamos una expresión regular para dividir la cadena por espacios que no están dentro de comillas
    palabras = re.split(r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', consola)

    # Eliminamos los espacios adicionales en cada palabra
    comandos = [palabra.strip() for palabra in palabras]

    return analizar_comandos(comandos)


def analizar_comandos(comandos_entrada):
    #VERIFICA QUE NO HAYAN ESPACIOS EN BLANCO
    for elemento in comandos_entrada:
        if elemento == "": return printError("Hay un espacio en blanco de más.")
            
    # VERIFICA SI VIENE UN PAUSE
    if comandos_entrada[0].lower() == "pause":
        return "pause"

    # TOMO TODOS LOS COMANDOS LUEGO DE EXECUTE Y EL COMANDO (mkdisk, rmdisk, etc)
    if len(comandos_entrada) <= 1 and comandos_entrada[0].lower() != "logout":
        return printError("No tiene parametros para ejecutar el comando {}".format(comandos_entrada[0]))

    match comandos_entrada.pop(0).lower():
        case "mkdisk":
            return comandos_mkdisk(comandos_entrada)

        case "rmdisk":
            return parametros_rmdisk(comandos_entrada)
        
        case "fdisk":
            return parametros_fdisk(comandos_entrada)
        
        case "mount":
            return parametros_mount(comandos_entrada)
        
        case "mkfs":
            return parametros_mkfs(comandos_entrada)
        
        case "login":
            return parametros_login(comandos_entrada)
        
        case "logout":
            return parametros_logout()
        
        case "mkgrp":
            return parametros_mkgrp(comandos_entrada)
        
        case "rmgrp":
            return parametros_rmgrp(comandos_entrada)
        
        case "mkusr":
            return parametros_mkusr(comandos_entrada)
        
        case "rmusr":
            return parametros_rmusr(comandos_entrada)
        
        case "mkdir":
            return parametros_mkdir(comandos_entrada)
        
        case "mkfile":
            return parametros_mkfile(comandos_entrada)
        
        case "rep":
            return parametros_rep(comandos_entrada)

        case _:
            return printError("El comando no existe.")
