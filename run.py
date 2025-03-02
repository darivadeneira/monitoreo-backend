from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from app.routes.resources import resources_socket, resources
from app.routes.auth import auth
from app.models.models import db
from threading import Thread
from dotenv import load_dotenv
import os
from app.routes.alerts import alerts  # Añadir esta línea

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
# Configurar CORS
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:5000",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5000"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        "supports_credentials": True
    }
})

# Configuración MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST'),
    os.getenv('DB_PORT'),
    os.getenv('DB_NAME')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio = SocketIO(app, 
                   cors_allowed_origins=[
                       "http://localhost:3000",
                       "http://localhost:5173",
                       "http://localhost:5000",
                       "http://127.0.0.1:3000",
                       "http://127.0.0.1:5173",
                       "http://127.0.0.1:5000"
                   ],
                   supports_credentials=True)
db.init_app(app)

# Registrar blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(resources, url_prefix='/resources')
app.register_blueprint(alerts, url_prefix='/alerts')

active_threads = {}

@socketio.on("connect")
def handle_connect():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return False
        
        user_id = int(user_id)
        
        if user_id in active_threads:
            print(f"Deteniendo hilo anterior para usuario {user_id}")
            active_threads[user_id] = False
        
        print(f"Cliente conectado - Usuario ID: {user_id}")
        thread = Thread(target=resources_socket, args=(socketio, app, user_id))
        thread.daemon = True
        active_threads[user_id] = True
        thread.start()
        return True
        
    except Exception as e:
        print(f"Error en conexión: {e}")
        return False

@socketio.on("disconnect")
def handle_disconnect():
    try:
        user_id = request.args.get('user_id')
        if user_id:
            user_id = int(user_id)
            if user_id in active_threads:
                active_threads[user_id] = False
                print(f"Cliente desconectado - Usuario ID: {user_id}")
    except Exception as e:
        print(f"Error en desconexión: {e}")
    print("Cliente desconectado")

def main():
    with app.app_context():
        db.create_all()
    print("Iniciando servidor...")
    socketio.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
