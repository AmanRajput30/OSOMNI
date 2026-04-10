import psutil
import time

# Initialize CPU measurement globally before API starts
psutil.cpu_percent(interval=None)

def get_system_stats():
    # interval=None calculates CPU utilization since last call
    cpu_percent = psutil.cpu_percent(interval=None)
    
    # Fallback to prevent 0.0% artifacts due to rapid concurrent API polling
    if cpu_percent <= 0.0:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    total = mem.total
    used = mem.used
    available = mem.available
    cached = getattr(mem, 'cached', 0)
    buffers = getattr(mem, 'buffers', 0)
    
    true_used = total - available
    true_percent = (true_used / total) * 100
    
    if available > 1 * 1024**3:
        status = "Healthy (High usage mostly cached)" if mem.percent > 80 else "System is using RAM efficiently"
    elif available < 500 * 1024**2:
        status = "Critical (Low available memory - performance may degrade)"
    else:
        status = "Moderate usage"
        
    # Intelligence Logic for CPU
    if cpu_percent < 5:
        cpu_status = "System is idle"
    elif cpu_percent > 80:
        cpu_status = "High load detected"
    else:
        cpu_status = "Normal usage"
        
    return {
        "cpu": {
            "percent": cpu_percent,
            "status": cpu_status
        },
        "memory": {
            "total": total,
            "used": used,
            "available": available,
            "cached": cached,
            "buffers": buffers,
            "true_used": true_used,
            "percent": mem.percent,
            "true_percent": round(true_percent, 1),
            "status": status
        },
        "disk": {
            "percent": disk.percent,
            "used": disk.used,
            "total": disk.total
        }
    }
