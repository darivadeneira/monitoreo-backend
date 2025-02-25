import psutil


def get_cpu_info():
    # Obtener porcentaje de uso de la CPU
    cpu = psutil.cpu_percent(interval=1)
    
    # Obtener la frecuencia del CPU
    freq = psutil.cpu_freq()
    cpu_freq = {
        'current': round(freq.current / 1000, 2) if freq else None,  # Convertir a GHz
        'min': round(freq.min / 1000, 2) if freq and hasattr(freq, 'min') else None,  # Convertir a GHz
        'max': round(freq.max / 1000, 2) if freq and hasattr(freq, 'max') else None  # Convertir a GHz
    }
    
    # Intentar obtener la temperatura del CPU
    cpu_temp = None  # Inicializar temperatura como None
    try:
        # Usar psutil para obtener la temperatura del CPU
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            core_temps = temps['coretemp']
            if core_temps:
                cpu_temp = core_temps[0].current  # Obtener la temperatura actual del primer núcleo
    except Exception as e:
        print(f"Error al obtener la temperatura: {e}")

    # Obtener lista de procesos
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            proc_info = proc.info
            process_list.append({
                'pid': proc_info['pid'],
                'name': proc_info['name'],
                'user': proc_info['username']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return {
        'cpu_percentage': cpu,
        'cpu_frequency': cpu_freq,
        'cpu_temperature': cpu_temp,  # Se devuelve la temperatura (si está disponible)
        'process_count': len(list(psutil.process_iter())),
        'processes': process_list
    }