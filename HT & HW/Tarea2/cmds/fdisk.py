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
     

    
    pass