from Reportes.Importaciones_rep import *

def _analizarReporte(tipoReporte, particionMount,  path_a_crear, pathMBR, rutaR_File):
    match tipoReporte:
        case "mbr":
            return reporteMBR(path_a_crear, pathMBR)

        case "disk":
            return reporteDISK(pathMBR, path_a_crear)

        case "file":
            return reporteFILE(particionMount, path_a_crear, rutaR_File)
        
        case "bm_inode":
            return reporteBM_INODE(particionMount, path_a_crear)
        
        case "bm_block":
            return reporteBM_BLOCK(particionMount, path_a_crear)
        
        case "sb":
            return reporteSB(particionMount, path_a_crear)
        
        case "tree":
            return reporteTREE(particionMount, path_a_crear)
        
        case _:
            return printError(f"El reporte -{tipoReporte} no existe.")


def parametros_rep(parametros):
    name, path_a_crear, id, rutaSA = "", "", "", ""

    for elemento in parametros:

        partes = elemento.split("=")
        # SI SU LONGITUD NO ES 2 NI EMPIEZA CON EL CARACTER -, SIGUE OTRA ITERACION
        if not(len(partes) == 2 and partes[0].startswith("-")):
            continue

        parametro = partes[0][1:]  # Eliminamos el "-"
        valor = partes[1]

        match parametro:
            case "path":
                valor = valor.replace('"', '')
                path_a_crear = valor

            case "name":
                name = valor

            case "id":
                id = valor

            case "ruta":
                rutaSA = valor.replace('"', '')

            case _:
                return printError(f"El parametro -{parametro} no existe.")
            
    #       <<<<<<<<<<<<<<<<<<<< VALIDACIONES >>>>>>>>>>>>>>>>>>>>
    
    particionesMontadas = ParticionesMontadas()
    particiones = particionesMontadas.obtenerParticiones()

    # VERIFICAR SI EL ID EXISTE
    existeID = False
    pathMBR = ""
    for particion in particiones:
        if id == particion["id"]:
            existeID = True
            pathMBR = particion["path"]
            break

    if existeID is False:
        return printError("La partición con el id: {}, no existe.".format(id))
    
    particionMount = particionesMontadas.returnPartMontada(id)

    # SI ESTA BIN, ANALIZARA QUE TIPO DE REPORTE ES
    try:
        return _analizarReporte(name.lower(), particionMount, path_a_crear, pathMBR, rutaSA)
    
    except Exception as e:
        print(e)
        return printError("Ocurrio un error al generar el reporte.")

