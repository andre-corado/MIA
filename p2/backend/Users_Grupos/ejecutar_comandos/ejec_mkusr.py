from General.Global import SesionActiva
from Users_Grupos.Comandos.mkusr import Mkusr
from Utilidades.utilidades import printError


def parametros_mkusr(parametros):
    sesionActiva = SesionActiva()
    user_, pass_, grp_  = "", "", ""

    for elemento in parametros:
        
        partes = elemento.split("=")
        # SI SU LONGITUD NO ES 2 NI EMPIEZA CON EL CARACTER -, SIGUE OTRA ITERACION
        if not(len(partes) == 2 and partes[0].startswith("-")):
            continue

        parametro = partes[0][1:]  # Eliminamos el "-"
        valor = partes[1]

        match parametro.lower():
            case "user":
                entrada_sin_comillas = valor.replace('"', '')
                user_ = entrada_sin_comillas
            
            case "pass":
                entrada_sin_comillas = valor.replace('"', '')
                pass_ = entrada_sin_comillas
            
            case "grp":
                entrada_sin_comillas = valor.replace('"', '')
                grp_ = entrada_sin_comillas

            case _:
                return printError(f"El parametro -{parametro} no existe.")
    

    #       <<<<<<<<<<<<<<<<<<<< VALIDACIONES >>>>>>>>>>>>>>>>>>>>

    # VERIFICAR QUE HAYA UNA SESION EXISTENTE
    if sesionActiva.getSesion_iniciada() is None:
        return printError("Para este comando se necesita iniciar sesión.")
    
    # VERIFICAR QUE SOLO EL USUARIO ROOT PUEDA EJECUTAR EL COMANDO
    if sesionActiva.getSesion_iniciada() != "root":
        return printError("Solo el usuario root puede ejecutar este comando.")
    
    # VERIFICAR QUE USER TENGA MAXIMO 10 CARACTERES
    if len(user_) > 10:
        return printError("El usuario debe tener como máximo 10 caracteres.")
    
    # VERIFICAR QUE PASS TENGA MAXIMO 10 CARACTERES
    if len(pass_) > 10:
        return printError("La contraseña debe tener como máximo 10 caracteres.")
  
    # VERIFICAR QUE EL GRUPO TENGA MAXIMO 10 CARACTERES
    if len(grp_) > 10:
        return printError("El grupo debe tener como máximo 10 caracteres.")

    
    # SI TODO ESTA BIEN, SE CREA EL USUARIO
    mkusr = Mkusr(user_, pass_, grp_)
    return mkusr.crearUsuario()
