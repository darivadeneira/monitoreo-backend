import psutil

def get_system_resources():
    cpu = psutil.cpu_percent(interval=1)
    
    process_act = psutil.process_iter()
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


    memory_info = psutil.virtual_memory()
    memory_used = memory_info.used / (1024 ** 2)  
    memory_total = memory_info.total / (1024 ** 2)  
    memory_percentage = memory_info.percent  

    processes = []
    
    for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info']):
        try:
            mem_info = proc.info['memory_info']
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'memory_mb': round(mem_info.rss / (1024 * 1024), 2) # Convertir a MB
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    processes = sorted(processes, key=lambda p: p['memory_mb'], reverse=True)
    
    disk_used = psutil.disk_usage('/').used / (1024 ** 3)  
    
    return {
        'cpu': cpu,
        'process_act': len(list(process_act)),
        'processes': process_list,  # Cambiamos cpu_process por processes
        'memory': {
            'used': round(memory_used, 2),
            'total': round(memory_total, 2),
            'percentage': memory_percentage,
        },
        'memory_processes': processes,
        'disk': round(disk_used, 2),
    }