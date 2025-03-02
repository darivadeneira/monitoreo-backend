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

def check_threshold(resource_type, value, user_id): 
    if value > threshold.get(resource_type, 80):
        alert = Alert(
            resource_type=resource_type,
            threshold=threshold[resource_type],
            current_value=value,
            user_id=user_id 
        )
        db.session.add(alert)
        db.session.commit()

def resources_socket(socketio, app, user_id):  
    is_connected = True
    
    def stop_monitoring():
        nonlocal is_connected
        is_connected = False

    socketio.on_event('disconnect', stop_monitoring)
    
    while is_connected:
        try:
            with app.app_context():
                system_resources = get_system_resources()
                
                usage = ResourceUsage(
                    cpu_percent=system_resources['cpu']['cpu_percentage'],
                    memory_percent=system_resources['memory']['percentage'],
                    disk_percent=psutil.disk_usage('/').percent,
                    user_id=user_id
                )
                db.session.add(usage)
                db.session.commit()
                
                check_threshold('cpu', system_resources['cpu']['cpu_percentage'], user_id)
                check_threshold('memory', system_resources['memory']['percentage'], user_id)
                check_threshold('disk', psutil.disk_usage('/').percent, user_id)
                
                data = {
                    'cpu': system_resources['cpu'],
                    'memory': system_resources['memory'],
                    'network': system_resources['network'],
                    'disk': system_resources['disk']
                }
                
                if is_connected:
                    socketio.emit('resources', data)
                else:
                    print(f"Monitoreo detenido para usuario {user_id}")
                    break
                    
            time.sleep(1)
        except Exception as e:
            print(f"Error en monitoreo: {e}")
            is_connected = False
            break

    print(f"Finalizando monitoreo para usuario {user_id}")