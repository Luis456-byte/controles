from flask import Flask, request, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, db

# Inicializa Firebase
cred = credentials.Certificate("credenciales.json")  # Asegúrate de tener este archivo en el mismo directorio
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://carrobot-3b7aa-default-rtdb.firebaseio.com/'  # Reemplaza con la URL de tu base de datos Firebase
})

app = Flask(__name__)

# Variable global para almacenar el último comando
ultimo_comando = {"mensaje": "Ninguna acción aún"}

@app.route('/')
def index():
    # Renderiza la página principal con el mensaje actual
    return render_template('index.html', mensaje=ultimo_comando["mensaje"])

@app.route('/enviar', methods=['POST'])
def enviar_comando():
    global ultimo_comando  # Accede a la variable global
    data = request.json
    command = data.get("comando")  # Asegúrate de que coincida con el JSON enviado

    if command in ['F', 'R', 'L', 'B']:
        # Traducción de comandos a texto
        acciones = {
            "F": "Adelante",
            "R": "Girar a la izquierda",
            "L": "Girar a la derecha",
            "B": "Retroceder"
        }

        # Actualiza Firebase
        ref = db.reference('carrito')
        ref.update({"accion": command})

        # Actualiza el último comando
        ultimo_comando["mensaje"] = acciones[command]

        return jsonify({"status": "success", "message": f"Comando '{acciones[command]}' enviado"}), 200
    else:
        return jsonify({"status": "error", "message": "Comando no válido"}), 400

if __name__ == '__main__':
    app.run(debug=True)
