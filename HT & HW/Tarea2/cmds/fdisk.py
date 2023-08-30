def execute(consoleLine):
    size = 0
    unit = 'K'
    path = ''
    name = ''
    type = 'P'
    fit = 'WF'
    delete = ''
    add = 0
    # Buscar parametros
    try:
        for i in range(len(consoleLine)):
            if consoleLine[i].startswith('-size='):
                size = int(consoleLine[i][6:])
                if size <= 0:
                    return 'Error: Size debe ser mayor a 0.'
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
            elif consoleLine[i].startswith('-delete='):
                delete = consoleLine[i][8:].upper()
                if delete != 'FULL':
                    return 'Error: Delete no válido.'
            elif consoleLine[i].startswith('-add='):
                add = int(consoleLine[i][5:])
                if add == 0:
                    return 'Error: Add no puede ser 0.'
                
    except:
        return 'Error: En ingreso de parámetros.'