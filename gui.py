import tkinter as tk
from tkinter import ttk

from system_info import get_system_info
from health_check import evaluate_health
from exporter import export_json, export_csv


# =========================================================
# FUNCTIONS
# =========================================================

def refresh_dashboard():
    data = get_system_info()
    health = evaluate_health(data)

    hostname_value.config(text=data["hostname"])
    os_value.config(
        text=f'{data["operating_system"]} {data["os_release"]}'
    )
    ip_value.config(text=data["ipv4_address"])

    cpu_usage = data["cpu_usage_percent"]
    ram_usage = data["ram_usage_percent"]
    disk_usage = data["disk_usage_percent"]

    cpu_value.config(text=f"{cpu_usage}%")
    ram_value.config(text=f"{ram_usage}%")
    disk_value.config(text=f"{disk_usage}%")

    cpu_bar["value"] = cpu_usage
    ram_bar["value"] = ram_usage
    disk_bar["value"] = disk_usage

    status = health["status"]
    status_value.config(text=status)

    if status == "HEALTHY":
        status_value.config(fg="#22c55e")
    elif status == "WARNING":
        status_value.config(fg="#f59e0b")
    else:
        status_value.config(fg="#ef4444")

    alerts_box.config(state="normal")
    alerts_box.delete("1.0", tk.END)

    for alert in health["alerts"]:
        alerts_box.insert(tk.END, f"• {alert}\n")

    alerts_box.config(state="disabled")

    action_status.config(
        text="System data refreshed successfully.",
        fg="#38bdf8"
    )


def export_json_report():
    try:
        filename = export_json()

        action_status.config(
            text=f"JSON saved: {filename}",
            fg="#22c55e"
        )

    except Exception as error:
        action_status.config(
            text=f"JSON export failed: {error}",
            fg="#ef4444"
        )


def export_csv_report():
    try:
        filename = export_csv()

        action_status.config(
            text=f"CSV saved: {filename}",
            fg="#22c55e"
        )

    except Exception as error:
        action_status.config(
            text=f"CSV export failed: {error}",
            fg="#ef4444"
        )


def create_metric(parent, label_text, row):
    tk.Label(
        parent,
        text=label_text,
        font=("Segoe UI", 11, "bold"),
        fg="white",
        bg="#0f172a"
    ).grid(
        row=row,
        column=0,
        sticky="w",
        pady=8
    )

    value_label = tk.Label(
        parent,
        text="0%",
        font=("Segoe UI", 11, "bold"),
        fg="#38bdf8",
        bg="#0f172a",
        width=8
    )
    value_label.grid(
        row=row,
        column=1,
        padx=10
    )

    progress_bar = ttk.Progressbar(
        parent,
        orient="horizontal",
        length=360,
        mode="determinate",
        maximum=100
    )
    progress_bar.grid(
        row=row,
        column=2,
        pady=8
    )

    return value_label, progress_bar


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("IT Asset Inventory Dashboard")

root.geometry("720x760")
root.minsize(720, 760)
root.configure(bg="#0f172a")


# =========================================================
# TITLE
# =========================================================

title = tk.Label(
    root,
    text="IT ASSET INVENTORY",
    font=("Segoe UI", 24, "bold"),
    fg="white",
    bg="#0f172a"
)
title.pack(pady=(20, 5))


subtitle = tk.Label(
    root,
    text="Windows System Health & Asset Dashboard",
    font=("Segoe UI", 11),
    fg="#94a3b8",
    bg="#0f172a"
)
subtitle.pack(pady=(0, 15))


# =========================================================
# SYSTEM INFORMATION
# =========================================================

info_frame = tk.Frame(
    root,
    bg="#1e293b",
    padx=20,
    pady=15
)
info_frame.pack(
    fill="x",
    padx=30,
    pady=8
)


tk.Label(
    info_frame,
    text="Hostname",
    fg="#94a3b8",
    bg="#1e293b",
    font=("Segoe UI", 10)
).grid(row=0, column=0, sticky="w")


hostname_value = tk.Label(
    info_frame,
    text="-",
    fg="white",
    bg="#1e293b",
    font=("Segoe UI", 10, "bold")
)
hostname_value.grid(
    row=0,
    column=1,
    sticky="w",
    padx=30
)


tk.Label(
    info_frame,
    text="Operating System",
    fg="#94a3b8",
    bg="#1e293b",
    font=("Segoe UI", 10)
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=6
)


os_value = tk.Label(
    info_frame,
    text="-",
    fg="white",
    bg="#1e293b",
    font=("Segoe UI", 10, "bold")
)
os_value.grid(
    row=1,
    column=1,
    sticky="w",
    padx=30
)


tk.Label(
    info_frame,
    text="IPv4 Address",
    fg="#94a3b8",
    bg="#1e293b",
    font=("Segoe UI", 10)
).grid(row=2, column=0, sticky="w")


ip_value = tk.Label(
    info_frame,
    text="-",
    fg="white",
    bg="#1e293b",
    font=("Segoe UI", 10, "bold")
)
ip_value.grid(
    row=2,
    column=1,
    sticky="w",
    padx=30
)


# =========================================================
# RESOURCE METRICS
# =========================================================

metrics_frame = tk.Frame(
    root,
    bg="#0f172a"
)
metrics_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


cpu_value, cpu_bar = create_metric(
    metrics_frame,
    "CPU Usage",
    0
)

ram_value, ram_bar = create_metric(
    metrics_frame,
    "RAM Usage",
    1
)

disk_value, disk_bar = create_metric(
    metrics_frame,
    "Disk Usage",
    2
)


# =========================================================
# HEALTH STATUS
# =========================================================

status_frame = tk.Frame(
    root,
    bg="#1e293b",
    padx=20,
    pady=12
)
status_frame.pack(
    fill="x",
    padx=30,
    pady=8
)


tk.Label(
    status_frame,
    text="Overall Health",
    font=("Segoe UI", 12, "bold"),
    fg="white",
    bg="#1e293b"
).pack(side="left")


status_value = tk.Label(
    status_frame,
    text="-",
    font=("Segoe UI", 16, "bold"),
    fg="white",
    bg="#1e293b"
)
status_value.pack(side="right")


# =========================================================
# HEALTH ALERTS
# =========================================================

alerts_label = tk.Label(
    root,
    text="Health Alerts",
    font=("Segoe UI", 12, "bold"),
    fg="white",
    bg="#0f172a"
)
alerts_label.pack(
    anchor="w",
    padx=30,
    pady=(12, 5)
)


alerts_box = tk.Text(
    root,
    height=4,
    bg="#111827",
    fg="#e5e7eb",
    font=("Consolas", 10),
    bd=0,
    padx=12,
    pady=8
)
alerts_box.pack(
    fill="x",
    padx=30
)
alerts_box.config(state="disabled")


# =========================================================
# ACTION BUTTONS
# =========================================================

buttons_frame = tk.Frame(
    root,
    bg="#0f172a"
)
buttons_frame.pack(
    pady=(18, 8)
)


refresh_button = tk.Button(
    buttons_frame,
    text="Refresh System Data",
    command=refresh_dashboard,
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    font=("Segoe UI", 10, "bold"),
    bd=0,
    width=18,
    padx=8,
    pady=10,
    cursor="hand2"
)
refresh_button.grid(
    row=0,
    column=0,
    padx=6
)


json_button = tk.Button(
    buttons_frame,
    text="Export JSON",
    command=export_json_report,
    bg="#7c3aed",
    fg="white",
    activebackground="#6d28d9",
    activeforeground="white",
    font=("Segoe UI", 10, "bold"),
    bd=0,
    width=14,
    padx=8,
    pady=10,
    cursor="hand2"
)
json_button.grid(
    row=0,
    column=1,
    padx=6
)


csv_button = tk.Button(
    buttons_frame,
    text="Export CSV",
    command=export_csv_report,
    bg="#0891b2",
    fg="white",
    activebackground="#0e7490",
    activeforeground="white",
    font=("Segoe UI", 10, "bold"),
    bd=0,
    width=14,
    padx=8,
    pady=10,
    cursor="hand2"
)
csv_button.grid(
    row=0,
    column=2,
    padx=6
)


# =========================================================
# ACTION STATUS
# =========================================================

action_status = tk.Label(
    root,
    text="Ready",
    font=("Segoe UI", 9),
    fg="#94a3b8",
    bg="#0f172a"
)
action_status.pack(
    pady=(4, 6)
)


# =========================================================
# FOOTER
# =========================================================

footer = tk.Label(
    root,
    text="Python IT Automation • Asset Inventory & System Health",
    font=("Segoe UI", 9),
    fg="#64748b",
    bg="#0f172a"
)
footer.pack(
    pady=(4, 12)
)


# =========================================================
# INITIAL LOAD
# =========================================================

refresh_dashboard()


# =========================================================
# START APPLICATION
# =========================================================

root.mainloop()