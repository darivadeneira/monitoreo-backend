import psutil

def get_system_resources():
    cpu = psutil.cpu_percent(interval=1)
    
    memory_info = psutil.virtual_memory()
    memory_used = memory_info.used / (1024 ** 2)  # Convertir a MB
    memory_total = memory_info.total / (1024 ** 2)  # Convertir a MB
    memory_percentage = memory_info.percent  # Uso en porcentaje
    
    disk_used = psutil.disk_usage('/').used / (1024 ** 3)  # Convertir a GB
    
    return {
        'cpu': cpu,
        'memory': {
            'used': round(memory_used, 2),
            'total': round(memory_total, 2),
            'percentage': memory_percentage
        },
        'disk': round(disk_used, 2)
    }
