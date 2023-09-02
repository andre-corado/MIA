import os.path
import struct
# Utilizar Graphviz
from graphviz import Digraph

from cmds.structs.MBR import MBR


def execute(consoleLine):
    name, path, id, ruta = '', '', '', ''
    nameFound, pathFound, idFound, rutaFound = False, False, False, False
    for i in range(len(consoleLine)):
        if consoleLine[i].startswith('-path='):
            path = consoleLine[i][6:]
            if len(path) < 5:
                return 'Error: Path no puede ser vacío.'
            pathFound = True
        if consoleLine[i].startswith('-name='):
            name = consoleLine[i][6:].upper()
            if len(name) < 1:
                return 'Error: Name no puede ser vacío.'
            nameFound = True
        if consoleLine[i].startswith('-id='):
            id = consoleLine[i][4:]
            if not id.endswith('.dsk') and not id.endswith('.dsk\"'):
                return 'Error: Id debe ser un archivo .dsk'
            if len(id) < 1:
                return 'Error: Id no puede ser vacío.'
            idFound = True
        if consoleLine[i].startswith('-ruta='):
            ruta = consoleLine[i][6:]
            if len(ruta) < 1:
                return 'Error: Ruta no puede ser vacío.'
            rutaFound = True

    if name == 'MBR':
        if not pathFound or not idFound:
            return 'Error: Faltan parámetros obligatorios.'
        return makeMBRTable(path, id)
    if name == 'DISK':
        if not pathFound or not idFound:
            return 'Error: Faltan parámetros obligatorios.'
        return makeDiskTable(path, id)


def makeMBRTable(tablePath, diskPath):
    # Leer disco
    if not os.path.exists(diskPath):
        return 'Error: No existe el disco.'
    with open(diskPath, "rb") as file:
        mbr = MBR()
        mbr.decode(file.read(136))
        file.close()
        if ".jpg" in tablePath or ".png" in tablePath or ".pdf" in tablePath:
            if not tablePath.endswith("\""):
                ext = tablePath[-3:]
                tablePath = tablePath[:-4]
            else:
                ext = tablePath[-4:-1]
                tablePath = tablePath[1:-5]
            dot = mbr.getGraph(ext)

            # Verificar si existe directorio y crearlo si no existe
            words = tablePath.split('/')
            dir = ''
            for i in range(len(words) - 1):
                dir += words[i] + '/'
            if os.path.exists(dir) == False:
                os.makedirs(dir)

            # Renderizar dot en table path
            dot.render(tablePath, view=True)

            # Borrar archivos temporales
            os.remove(tablePath)
        else:
            return 'Error: Formato de reporte no válido.'
    file.close()
    return 'Tabla MBR creada exitosamente.'

def makeDiskTable(path, id):
    pass