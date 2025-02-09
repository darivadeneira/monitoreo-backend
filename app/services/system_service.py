import psutil

def get_system_resources():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().used / (1024 ** 2)
    disk = psutil.disk_usage('/').used / (1024 ** 3)
    return {
        'cpu': cpu,
        'memory': memory,
        'disk': disk
    }
