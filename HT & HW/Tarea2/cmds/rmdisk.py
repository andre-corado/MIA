def execute(consoleLine):
    path = consoleLine[1].split("=")[1]
    if not os.path.exists(path):
        return "Error: El disco no existe."
    os.remove(path)
    return "Disco eliminado exitosamente.\n"