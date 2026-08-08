from system_info import get_system_info


def evaluate_health(data):
    alerts = []
    status = "HEALTHY"

    cpu = data["cpu_usage_percent"]
    ram = data["ram_usage_percent"]
    disk = data["disk_usage_percent"]

    # CPU
    if cpu >= 90:
        alerts.append(f"CRITICAL: CPU usage is {cpu}%")
        status = "CRITICAL"
    elif cpu >= 75:
        alerts.append(f"WARNING: CPU usage is {cpu}%")
        if status != "CRITICAL":
            status = "WARNING"

    # RAM
    if ram >= 90:
        alerts.append(f"CRITICAL: RAM usage is {ram}%")
        status = "CRITICAL"
    elif ram >= 75:
        alerts.append(f"WARNING: RAM usage is {ram}%")
        if status != "CRITICAL":
            status = "WARNING"

    # Disk
    if disk >= 90:
        alerts.append(f"CRITICAL: Disk usage is {disk}%")
        status = "CRITICAL"
    elif disk >= 80:
        alerts.append(f"WARNING: Disk usage is {disk}%")
        if status != "CRITICAL":
            status = "WARNING"

    if not alerts:
        alerts.append("No resource alerts detected.")

    return {
        "status": status,
        "alerts": alerts
    }


if __name__ == "__main__":
    system_data = get_system_info()
    health = evaluate_health(system_data)

    print("\n=== SYSTEM HEALTH ===\n")
    print(f"Overall Status: {health['status']}")

    print("\nAlerts:")
    for alert in health["alerts"]:
        print(f"- {alert}")