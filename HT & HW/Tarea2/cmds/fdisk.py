import os
from cmds.structs.MBR import MBR, Partition


def execute(consoleLine):
    size = 0
    unit = 'K'
    path = ''
    name = ''
    type = 'P'
    fit = 'WF'
    delete = ''
    add = 0
    
    #     status='N', type='P', fit='F', start=-1, size=0, name=''):

    # Buscar parametros
    try:
        sizeFound, deleteFound, addFound = False, False, False
        for i in range(len(consoleLine)):
            if consoleLine[i].startswith('-size='):
                size = int(consoleLine[i][6:])
                if size <= 0:
                    return 'Error: Size debe ser mayor a 0.'
                if not deleteFound and not addFound:
                    sizeFound = True
            elif consoleLine[i].startswith('-path='):
                path = consoleLine[i][6:]
                if path.endswith('.dsk') == False:
                    return 'Error: Path debe ser un archivo .dsk'
                if len(path) < 5:
                    return 'Error: Path no puede ser vacío.'
            elif consoleLine[i].startswith('-name='):
                name = consoleLine[i][6:]
                if len(name) < 1:
                    return 'Error: Name no puede ser vacío.'
            elif consoleLine[i].startswith('-unit='):
                unit = consoleLine[i][6:].upper()
                if unit != 'B' and unit != 'K' and unit != 'M':
                    return 'Error: Unit no válida.'
            elif consoleLine[i].startswith('-type='):
                type = consoleLine[i][6:].upper()
                if type != 'P' and type != 'E' and type != 'L':
                    return 'Error: Type no válido.'                
            elif consoleLine[i].startswith('-fit='):
                fit = consoleLine[i][5:].upper()
                if fit != 'BF' and fit != 'FF' and fit != 'WF':
                    return 'Error: Fit no válido.'
                else:
                    if fit == 'BF':
                        fit = 'B'
                    elif fit == 'FF':
                        fit = 'F'
                    elif fit == 'WF':
                        fit = 'W'
            elif consoleLine[i].startswith('-delete='):
                delete = consoleLine[i][8:].upper()
                if delete != 'FULL':
                    return 'Error: Delete no válido.'
                if not sizeFound and not addFound:
                    deleteFound = True
            elif consoleLine[i].startswith('-add='):
                add = int(consoleLine[i][5:])
                if add == 0:
                    return 'Error: Add no puede ser 0.'
                if not sizeFound and not deleteFound:
                    addFound = True
        
        if sizeFound:
            # Se crea una partición
            if unit == 'K':
                size *= 1024
            elif unit == 'M':
                size *= 1024 * 1024
            newPartition(size, path, name, type, fit)
            pass
        elif addFound:
            # Se modifica el tamaño de una partición
            pass
        elif deleteFound:
            # Se elimina una partición
            pass
    except:
        return 'Error: En ingreso de parámetros.'
    

def newPartition(size, path, name, type, fit):
    try:
        if not os.path.exists(path):
            return 'Error: Disco no encontrado.'
        file = open(path, 'rb+')
        # Leer MBR
        mbr = MBR()
        mbr.decode(file.read(136))
        file.close()

        # Validar que no exista una partición con el mismo nombre
        if mbr.hasPartitionNamed(name):
            return 'Error: Ya existe una partición con ese nombre.'
        
        # Primarias y extendidas
        if type == 'P' or type == 'E':            
            if type == 'E' and mbr.hasExtendedPartition(): # Solo puede haber una extendida
                return 'Error: Ya existe una partición extendida.'
            if mbr.canAddPartition(size) == False: # Solo pueden haber 4 particiones primarias y debe caber la nueva
                return 'Error: No se puede crear la partición.\nNo hay espacio suficiente o las 4 particiones primarias ya están creadas.' 
            
            # FF - First Fit
            # calcular start
            index = mbr.getPartitionIndexForFF(size)
            


            newPart = Partition('E', type, fit, start, size, name)

        # Lógicas
        if type == 'L':
            if not mbr.hasExtendedPartition():
                return 'Error: No existe una partición extendida aún para una partición lógica.'



    except:
        return 'Error: Disco no encontrado.'
    
    