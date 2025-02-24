import psutil
import time
import socket

def get_network_speed():
    # Primera medición
    counters_start = psutil.net_io_counters()
    bytes_sent_start = counters_start.bytes_sent
    bytes_recv_start = counters_start.bytes_recv
    
    # Esperar un segundo
    time.sleep(1)
    
    # Segunda medición
    counters_end = psutil.net_io_counters()
    bytes_sent_end = counters_end.bytes_sent
    bytes_recv_end = counters_end.bytes_recv
    
    # Calcular velocidad en MB/s
    upload_speed = (bytes_sent_end - bytes_sent_start) / (1024 * 1024)
    download_speed = (bytes_recv_end - bytes_recv_start) / (1024 * 1024)
    
    # Calcular uso total de red en MB
    total_sent = bytes_sent_end / (1024 * 1024)
    total_recv = bytes_recv_end / (1024 * 1024)
    
    # Obtener aplicaciones usando la red
    net_apps = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.connections(kind='inet'):  # Solo conexiones de internet
                net_apps.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name']
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Obtener interfaces activas
    active_interfaces = {}
    for interface, stats in psutil.net_if_stats().items():
        if stats.isup:  # Solo interfaces activas
            counters = psutil.net_io_counters(pernic=True).get(interface)
            if counters:
                total_traffic = (counters.bytes_sent + counters.bytes_recv) / (1024 * 1024)  # MB
                active_interfaces[interface] = {
                    'speed': stats.speed,
                    'total_traffic': round(total_traffic, 2)
                }

    return {
        'upload_speed': round(upload_speed, 2),    # MB/s
        'download_speed': round(download_speed, 2),  # MB/s
        'total_sent': round(total_sent, 2),        # MB
        'total_recv': round(total_recv, 2),        # MB
        'network_apps': net_apps,
        'active_interfaces': active_interfaces,
        'total_traffic': round((total_sent + total_recv), 2)  # MB
    }

def get_client_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Error al obtener IP del cliente: {e}")
        return None