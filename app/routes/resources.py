from flask_socketio import emit
from ..services.system_service import get_system_resources
import time

def resources_socket(socketio):
    try:
        while True:
            resources = get_system_resources()
            socketio.emit('resources', resources)
            time.sleep(1)
    except Exception as e:
        print(f"Error en resources_socket: {str(e)}")
