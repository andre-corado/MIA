import re

TAM_SB = 80
TAM_INODO = 101
TAM_EBR = 31
TAM_BLOQUE = 64

def printConsola(text): return("<System> {}" .format(text))

def printError(error): return("\t<<<Ocurrio un error>>> {}" .format(error))

def printSuccess(success): return("\t<<<Ejecutado>>> {}" .format(success))

def printPause(pause): return("\033[93m\t\t<Pause> {}\033[0m" .format(pause))

# QUITAR LAS COMILLAS DE UN PARAMETRO
def quitarComillas(cadena):
    try:
        contenido = re.search(r'"([^"]*)"', cadena)

        if contenido:
            return contenido.group(1)
        
        else:
            return cadena
        
    except Exception:
        return print(printError("Ocurrio un error en la cadena."))
