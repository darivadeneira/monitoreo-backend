import psutil
import time

def get_network_speed():
    # Primera medición
    bytes_sent_start = psutil.net_io_counters().bytes_sent
    bytes_recv_start = psutil.net_io_counters().bytes_recv
    
    # Esperar un segundo
    time.sleep(1)
    
    # Segunda medición
    bytes_sent_end = psutil.net_io_counters().bytes_sent
    bytes_recv_end = psutil.net_io_counters().bytes_recv
    
    # Calcular velocidad en MB/s
    upload_speed = (bytes_sent_end - bytes_sent_start) / (1024 * 1024)
    download_speed = (bytes_recv_end - bytes_recv_start) / (1024 * 1024)
    
    return {
        'upload_speed': round(upload_speed, 2),    # MB/s
        'download_speed': round(download_speed, 2)  # MB/s
    }
