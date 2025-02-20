import psutil

def get_cpu_info():
    cpu = psutil.cpu_percent(interval=1)
    
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
        'process_count': len(list(psutil.process_iter())),
        'processes': process_list
    }
