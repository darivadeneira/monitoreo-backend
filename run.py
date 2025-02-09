from flask import Flask
from flask_socketio import SocketIO
from app.routes.resources import resources_socket
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("connect")
def handle_connect():
    print("Cliente conectado")
    # Iniciar el envío de datos en un hilo separado
    Thread(target=resources_socket, args=(socketio,)).start()

@socketio.on("disconnect")
def handle_disconnect():
    print("Cliente desconectado")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000)
