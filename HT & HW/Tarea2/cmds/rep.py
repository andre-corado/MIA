import os.path
import struct
# Utilizar Graphviz
from graphviz import Digraph

from cmds.structs.MBR import MBR


def execute(consoleLine):
    name, path, id, ruta = '', '', '', ''
    for i in range(len(consoleLine)):
        if consoleLine[i].startswith('-path='):
            path = consoleLine[i][6:]
            if len(path) < 5:
                return 'Error: Path no puede ser vacío.'
        if consoleLine[i].startswith('-name='):
            name = consoleLine[i][6:].upper()
            if len(name) < 1:
                return 'Error: Name no puede ser vacío.'
        if consoleLine[i].startswith('-id='):
            id = consoleLine[i][4:]
            if not id.endswith('.dsk') and not id.endswith('.dsk\"'):
                return 'Error: Id debe ser un archivo .dsk'
            if len(id) < 1:
                return 'Error: Id no puede ser vacío.'
        if consoleLine[i].startswith('-ruta='):
            ruta = consoleLine[i][6:]
            if len(ruta) < 1:
                return 'Error: Ruta no puede ser vacío.'

    if name == 'MBR':
        return makeMBRTable(path, id)




def makeMBRTable(tablePath, diskPath):
    # Leer disco
    if not os.path.exists(diskPath):
        return 'Error: No existe el disco.'
    with open(diskPath, "rb") as file:
        mbr = MBR()
        mbr.decode(file.read(136))
        if tablePath.endswith('.jpg'):
            # render en jpg
            mbr.getGraph().render('MBR', view=True, format='jpg')
        elif tablePath.endswith('.png'):
            mbr.getGraph().render('MBR', view=True, format='png')
        elif tablePath.endswith('.pdf'):
            mbr.getGraph().render('MBR', view=True, format='pdf')
        elif tablePath.endswith('.svg'):
            mbr.getGraph().render('MBR', view=True, format='svg')
        else:
            file.close()
            return 'Error: Formato de reporte no válido.'
    file.close()
    return 'Tabla MBR creada exitosamente.'
