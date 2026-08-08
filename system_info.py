import getpass
import platform
import socket
from datetime import datetime

import psutil


def bytes_to_gb(value):
    return round(value / (1024 ** 3), 2)


def get_ip_address():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except socket.error:
        return "Unavailable"


def get_system_info():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("C:\\")
    boot_time = datetime.fromtimestamp(psutil.boot_time())

    information = {
        "hostname": socket.gethostname(),
        "username": getpass.getuser(),
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor() or "Unavailable",
        "cpu_cores_physical": psutil.cpu_count(logical=False),
        "cpu_cores_logical": psutil.cpu_count(logical=True),
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "ram_total_gb": bytes_to_gb(memory.total),
        "ram_used_gb": bytes_to_gb(memory.used),
        "ram_usage_percent": memory.percent,
        "disk_total_gb": bytes_to_gb(disk.total),
        "disk_used_gb": bytes_to_gb(disk.used),
        "disk_free_gb": bytes_to_gb(disk.free),
        "disk_usage_percent": disk.percent,
        "ipv4_address": get_ip_address(),
        "system_boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return information


if __name__ == "__main__":
    data = get_system_info()

    print("\n=== IT ASSET INVENTORY ===\n")

    for key, value in data.items():
        label = key.replace("_", " ").title()
        print(f"{label}: {value}")