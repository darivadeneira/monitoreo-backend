import psutil

def get_memory_info():
    memory_info = psutil.virtual_memory()
    memory_used = memory_info.used / (1024 ** 2)
    memory_total = memory_info.total / (1024 ** 2)
    
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info']):
        try:
            mem_info = proc.info['memory_info']
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'memory_mb': round(mem_info.rss / (1024 * 1024), 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    processes = sorted(processes, key=lambda p: p['memory_mb'], reverse=True)
    
    return {
        'used': round(memory_used, 2),
        'total': round(memory_total, 2),
        'percentage': memory_info.percent,
        'processes': processes
    }
