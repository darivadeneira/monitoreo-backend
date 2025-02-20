import psutil
import subprocess


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
    try:
        # Ejecutar el comando `sensors` y obtener la salida
        output = subprocess.check_output("sensors", shell=True).decode("utf-8")
        # Procesar la salida para encontrar la temperatura del CPU
        for line in output.splitlines():
            if "Core" in line:  # Buscar las líneas que contienen información del CPU
                temp = line.split(":")[1].strip().split()[0]
                return temp
        return None  # Si no se encuentra la temperatura
    except Exception as e:
        print(f"Error al obtener la temperatura: {e}")
        return None

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
        'cpu_temperature': cpu_temp,
        'process_count': len(list(psutil.process_iter())),
        'processes': process_list
    }

# Llamada a la función de ejemplo
cpu_info = get_cpu_info()
print(cpu_info)
