from General.Global import SesionActiva
from Users_Grupos.Comandos.mkgrp import Mkgrp
from Utilidades.utilidades import printError


def parametros_mkgrp(parametros):
    sesionActiva = SesionActiva()
    name  = ""

    for elemento in parametros:
        
        partes = elemento.split("=")
        # SI SU LONGITUD NO ES 2 NI EMPIEZA CON EL CARACTER -, SIGUE OTRA ITERACION
        if not(len(partes) == 2 and partes[0].startswith("-")):
            continue

        parametro = partes[0][1:]  # Eliminamos el "-"
        valor = partes[1]

        match parametro.lower():
            case "name":
                entrada_sin_comillas = valor.replace('"', '')
                name = entrada_sin_comillas

            case _:
                return printError(f"El parametro -{parametro} no existe.")
    

    #       <<<<<<<<<<<<<<<<<<<< VALIDACIONES >>>>>>>>>>>>>>>>>>>>

    # VERIFICAR QUE HAYA UNA SESION EXISTENTE
    if sesionActiva.getSesion_iniciada() is None:
        return printError("Para este comando se necesita iniciar sesión.")
    
    # VERIFICAR QUE SOLO EL USUARIO ROOT PUEDA EJECUTAR EL COMANDO
    if sesionActiva.getSesion_iniciada() != "root":
        return printError("Solo el usuario root puede ejecutar este comando.")
    
    # VERIFICAR QUE EL NOMBRE SEA MENOR A 10 CARACTERES
    if len(name) > 10:
        return printError("Solo se aceptan grupos con al menos 10 caracteres.")

    # SE CREA EL GRUPO 
    mkgrp = Mkgrp(name)
    return mkgrp.crearGrupo()
