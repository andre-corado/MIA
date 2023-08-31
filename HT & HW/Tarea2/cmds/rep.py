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
        with open(diskPath, "rb") as file:
            mbr = MBR()
            mbr.decode(file.read(136))
            mbr.getGraph().render('MBR', view=True)
            # guardar imagen jpg en tablePath
            return 'Tabla MBR creada exitosamente.'
        file.close()
