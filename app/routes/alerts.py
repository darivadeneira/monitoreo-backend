import datetime
from flask import Blueprint, request, jsonify
from app.models.models import db, Alert

alerts = Blueprint('alerts', __name__)

@alerts.route('/create', methods=['POST'])
def create_alert():
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['resource_type', 'threshold', 'current_value']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Se requieren: tipo de recurso, umbral y valor actual'}), 400

        # Crear nueva alerta
        new_alert = Alert(
            resource_type=data['resource_type'],
            threshold=float(data['threshold']),
            current_value=float(data['current_value']),
        )
        
        # Guardar en base de datos
        db.session.add(new_alert)
        db.session.commit()
        
        # Retornar alerta creada
        return jsonify({
            'message': 'Alerta creada exitosamente',
            'alert': {
                'id': new_alert.id,
                'resource_type': new_alert.resource_type,
                'threshold': new_alert.threshold,
                'current_value': new_alert.current_value,
                'timestamp': new_alert.timestamp.isoformat()
            }
        }), 201
        
    except ValueError:
        return jsonify({'error': 'Valores numéricos inválidos'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
