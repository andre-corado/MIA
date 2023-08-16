from cmds import * # Importar módulo de comandos
from cmds import mkdisk, rep


def split_Command(inputTxt):  # ANALIZADOR LÉXICO EN TEORÍA

    words = inputTxt.split(" ")
    words2 = []

    for i in range(len(words)):  # Se analiza cada palabra

        # ------------- COMILLAS DOBLE O SIMPLE -------------

        if words[i].startswith('"') or words[i].startswith("'"):
            # Si también termina con comillas dobles o simples
            if words[i].endswith('"') or words[i].endswith("'") and len(words[i]) > 1:
                words2.append(words[i])
            else:  # Sino se busca el siguiente elemento que termine con comillas
                for j in range(i + 1, len(words)):
                    if words[j].endswith('"') or words[j].endswith("'"):
                        # Unir palabras desde i hasta j
                        w = ""
                        for k in range(i, j + 1):
                            if k is not j and words[k] != "'""":
                                w = w + words[k] + " "
                            else:
                                w = w + words[k]
                        words2.append(w)
                        break
                else:  # Sino la encontró
                    return "Error: Comillas no cerradas"

        else:  # SE REALIZA UPPERCASE A LAS PALABRAS
            words2.append(words[i].lower())
    return analizar_Comando(words2);


def analizar_Comando(consoleLine):
    # ------------- COMANDO EXECUTE -------------
    if consoleLine[0] == "execute":
        # Si contiene -path= y tiene un path válido
        if consoleLine[1].startswith(">path=") and len(consoleLine[1]) > 6:
            # Obtener path
            path = consoleLine[1][6:]
            # tratar de leer el archivo y obtener String
            try:
                file = open(path, "r")
                text = file.read()
                file.close()
            except:
                return "Error: No se pudo leer el archivo"
            # Separar líneas
            lines = text.split("\n")
            # Analizar cada línea
            for line in lines:
                print(split_Command(line))
        return "Comando execute ejecutado.\n"

    # ------------- COMANDO MKDISK -------------
    elif consoleLine[0] == "mkdisk":
        return mkdisk.execute(consoleLine)

    # ------------- COMANDO REP -------------
    elif consoleLine[0] == "rep":
        return rep.execute()

    # ------------- COMANDO EXIT -------------
    elif consoleLine[0] == "exit":
        return "Comando exit reconocido.\n"

    # ------------- COMANDO NO RECONOCIDO -------------
    return "Comando no reconocido\n"
