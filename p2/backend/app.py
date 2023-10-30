from Users_Grupos.ejecutar_comandos.ejec_login import parametros_login
from Users_Grupos.ejecutar_comandos.ejec_logout import parametros_logout
from General.analizador import leerComando
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

@app.route('/')
def hello():
    return jsonify({'message': 'Hello, World!'})

# ENDPOINT: Analizar comandos
@app.route('/api-execute', methods=['POST'])
def execute():
    # Obtenemos el JSON de la petición
    data = request.get_json()
    valorDeEntrada = data.get('entrada')

    # Obtenemos la salida del analizador
    salida = leerComando(valorDeEntrada)# mkdisk -size=1 -path="/tmp/eliminar 1.dsk"
    output = ""

    if salida == 'pause':
        output = salida
    else:
        output = ' ' + salida + '\n\n'

    return jsonify({'salida': output})

# ENDPOINT: Login
@app.route('/api-login', methods=['POST'])
def execute_login():
    # Obtenemos el JSON de la petición
    data = request.get_json()
    valorDeEntrada = data.get('entrada').split(" ")
    valorDeEntrada.pop(0)

    # Obtenemos la salida del analizador
    salida = parametros_login(valorDeEntrada) # TRUE FALSE
    
    return jsonify({'salida': salida})

# ENDPOINT: Logout
@app.route('/api-logout', methods=['POST'])
def execute_logout():
    # Obtenemos el JSON de la petición
    data = request.get_json()
    valorDeEntrada = data.get('entrada')

    salida = parametros_logout()

    return jsonify({'salida': salida})

# ENDPOINT: Reporte
@app.route('/api-reporte/<nombre_archivo>', methods=['GET'])
def generate_image(nombre_archivo):
    # Devuelve la imagen como archivo adjunto
    imagen_path = './Reportes/Reportes_svg/' + nombre_archivo
    return send_file(imagen_path, as_attachment=True, download_name=nombre_archivo)

if __name__ == '__main__':
    app.run(host= 'localhost',port= 8000,)
