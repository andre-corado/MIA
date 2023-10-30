from Utilidades.utilidades import printSuccess
import os
import graphviz

def creacionImagen(pathImagen, codigo_dot):
    # Obtener el nombre del archivo y la extensión
    nombre_archivo, _ = os.path.splitext(os.path.basename(pathImagen))
    svg_path = './Reportes/Reportes_svg/' + nombre_archivo


    # ESCRIBO EL ARCHIVO TXT 
    documento = './Reportes/Reportes_svg/dotTXT/' + nombre_archivo + ".txt"
    
    with open(documento, 'w') as grafica:
        grafica.write(codigo_dot)

    # Crear un objeto Graphviz
    graph = graphviz.Source(codigo_dot)

    # Generar la gráfica en formato SVG
    graph.render(filename=svg_path, format="svg", cleanup=True)


# Genera un archivo SVG a partir de un código DOT
# Utiliza la librería Graphviz de Python
def generate_dot(dot_code: str, output_path: str, output_name: str):
    try:
        # ESCRIBO EL ARCHIVO TXT 
        documento = './Reportes/Reportes_svg/dotTXT/' + output_name + ".txt"
        
        with open(documento, 'w') as grafica:
            grafica.write(dot_code)

        # Crear un objeto Graphviz
        graph = graphviz.Source(dot_code)

        # Generar la gráfica en formato SVG
        svg_path = f"./Reportes/Reportes_svg/{output_name}"
        graph.render(filename=svg_path, format="svg", cleanup=True)

        return printSuccess("Reporte TREE generado correctamente!")
    except Exception as e:
        return f"Error al generar la gráfica: {str(e)}"