import psutil
from .resources.cpu_service import get_cpu_info
from .resources.memory_service import get_memory_info
from .resources.network_service import get_network_speed

def get_system_resources():
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    network_info = get_network_speed()
    disk_used = psutil.disk_usage('/').used / (1024 ** 3)
    
    return {
        'cpu': cpu_info,
        'process_act': cpu_info['process_count'],
        'processes': cpu_info['processes'],
        'memory': memory_info,
        'network': network_info,
        'disk': round(disk_used, 2),
    }