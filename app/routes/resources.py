from flask_socketio import emit
from flask import Blueprint, request, jsonify
import psutil
import time
from app.models.models import db, ResourceUsage, Alert
from ..services.system_service import get_system_resources

resources = Blueprint('resources', __name__)
threshold = {'cpu': 80, 'memory': 80, 'disk': 80}

@resources.route('/threshold', methods=['POST'])
def set_threshold():
    data = request.get_json()
    threshold.update(data)
    return jsonify({'message': 'Threshold updated successfully'}), 200

def check_threshold(resource_type, value):
    if value > threshold.get(resource_type, 80):
        alert = Alert(
            resource_type=resource_type,
            threshold=threshold[resource_type],
            current_value=value
        )
        db.session.add(alert)
        db.session.commit()

from flask import current_app

def resources_socket(socketio, app):
    while True:
        with app.app_context():
            system_resources = get_system_resources()
            
            # Guardar datos
            usage = ResourceUsage(
                cpu_percent=system_resources['cpu']['cpu_percentage'],
                memory_percent=system_resources['memory']['percentage'],
                disk_percent=psutil.disk_usage('/').percent
            )
            db.session.add(usage)
            db.session.commit()
            
            # Verificar umbrales
            check_threshold('cpu', system_resources['cpu']['cpu_percentage'])
            check_threshold('memory', system_resources['memory']['percentage'])
            check_threshold('disk', psutil.disk_usage('/').percent)
            
            # Preparar datos para enviar al cliente
            data = {
                'cpu': system_resources['cpu'],
                'memory': system_resources['memory'],
                'network': system_resources['network'],
                'disk': system_resources['disk']
            }
            socketio.emit('resources', data)
        time.sleep(1)