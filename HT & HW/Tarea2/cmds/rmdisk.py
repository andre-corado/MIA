import os
import time


def execute(consoleLine):
    path = consoleLine[1][6:]
    if path.endswith('.dsk') == False:
        if path.endswith('.dsk\"') == False:
            return 'Error: Path debe ser un archivo .dsk'
    if path.startswith('\"'):
        path = path[1:-1]
        if not os.path.exists(path):
            return 'Error: El disco no existe.'
    else:
        if not os.path.exists(path):
            return 'Error: El disco no existe.'

    print('Eliminando disco en: ' + path + '...')
    # pintar puntos suspensivos
    os.remove(path)
    return "Disco eliminado exitosamente.\n"