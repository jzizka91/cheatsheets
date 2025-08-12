
import socket
import time
import json
import os
import requests
from datetime import datetime, timedelta

try:
    from zoneinfo import ZoneInfo
except ImportError:
    print("This script requires Python 3.9+ for zoneinfo. Use pytz instead if needed.")
    exit(1)

from colorama import Fore, Style, init
init(autoreset=True)

# Configuration
AUTH_SERVER_IP = "game.project-epoch.net"
WORLD_SERVER_IP = "51.77.108.104"
SERVER_AUTH_PORT = 3724
SERVER_WORLD_PORT = 8085
DISCORD_WEBHOOK_URL = "<DISCORD_LINK>"
PUSHOVER_TOKEN = "<PUSHOVER_TOKEN>"
PUSHOVER_USER = "<PUSHOVER_USER>"
TIMEZONE = ZoneInfo("Europe/Prague")
STATE_FILE = "server_status.json"
LOG_DIR = "logs"
SERVER_NAME = "Kezan"

ENABLE_PUSHOVER = True
ENABLE_LAUNCHER_CHECK = True

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def get_current_time():
    return datetime.now(TIMEZONE)

def format_duration(delta):
    total_seconds = int(delta.total_seconds())
    if total_seconds < 60:
        return "<1m"
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    return ' '.join(parts)

def get_current_launcher_version():
    try:
        response = requests.get("https://updater.project-epoch.net/api/v2/manifest?environment=production", timeout=10)
        response.raise_for_status()
        manifest = response.json()
        return manifest.get("Version")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch launcher version: {e}")
        return None

def notify_discord_online(previous_downtime):
    duration_str = format_duration(previous_downtime)
    payload = {
        "content": f"🟢 ONLINE     📉 Down for:  `{duration_str}`",
        "username": "Kezan Status"
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send ONLINE webhook: {e}")

def notify_discord_offline(previous_uptime):
    duration_str = format_duration(previous_uptime)
    payload = {
        "content": f"🔴 OFFLINE   📈 Up for:  `{duration_str}`",
        "username": "Kezan Status"
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send OFFLINE webhook: {e}")

def notify_discord_launcher_update(new_version):
    payload = {
        "content": f"🛠️ New Update Available! (`{new_version}`)",
        "username": "Kezan Status"
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Discord launcher update: {e}")

def is_port_open(ip, port, timeout=5):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error):
        return False

def world_server_sent_data(ip, port, timeout=10):
    try:
        with socket.create_connection((ip, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            try:
                data = sock.recv(1024)
                return bool(data)
            except socket.timeout:
                return False
            except Exception as e:
                print(f"Error receiving data from world server: {e}")
                return False
    except (socket.timeout, socket.error):
        return False

def log_status(timestamp, auth_ok, world_ok, status):
    auth_status = "✅" if auth_ok else "❌"
    world_status = "✅" if world_ok else "SKIP" if not auth_ok else "❌"
    status_icon = "🟢" if status == "ONLINE" else "🔴"
    log_line = f"{timestamp} - AUTH: {auth_status}  WORLD: {world_status}  STATUS: {status_icon} {status}"
    log_filename = f"server_log_{timestamp.split()[0]}.txt"
    log_path = os.path.join(LOG_DIR, log_filename)
    with open(log_path, "a") as f:
        f.write(log_line + "\n")

def log_launcher_update(timestamp, version):
    log_line = f"{timestamp} - 🛠️ NEW LAUNCHER VERSION: {version}"
    log_filename = f"server_log_{timestamp.split()[0]}.txt"
    log_path = os.path.join(LOG_DIR, log_filename)
    with open(log_path, "a") as f:
        f.write(log_line + "\n")

def load_state():
    if not os.path.isfile(STATE_FILE):
        return {
            "last_state": None,
            "last_online_start": None,
            "last_offline_start": None,
            "pushover_sent": False,
            "last_launcher_version": None
        }
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def parse_time(ts):
    return datetime.fromisoformat(ts) if ts else None

def notify_pushover_online(duration):
    if not ENABLE_PUSHOVER:
        return
    duration_str = format_duration(duration)
    message = f"🟢 {SERVER_NAME} is ONLINE\nDown for: {duration_str}"
    payload = {
        "token": f"{PUSHOVER_TOKEN}",
        "user": f"{PUSHOVER_USER}",
        "message": message,
        "title": f"{SERVER_NAME} Server Online",
        "priority": 2,
        "retry": 60,
        "expire": 3600,
        "sound": "persistent"
    }
    print(f"🔔 Sending Pushover ONLINE alert... (Down for: {duration_str})")
    try:
        response = requests.post("https://api.pushover.net/1/messages.json", data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Pushover notification: {e}")

def notify_pushover_launcher_update(new_version):
    if not ENABLE_PUSHOVER:
        return
    message = f"🛠️ New Update Available! (`{new_version}`)"
    payload = {
        "token": f"{PUSHOVER_TOKEN}",
        "user": f"{PUSHOVER_USER}",
        "message": message,
        "title": f"{SERVER_NAME} Launcher Update",
        "priority": 1,
        "retry": 60,
        "expire": 3600,
        "sound": "gamelan"
    }
    print(f"🔔 Sending Pushover Launcher UPDATE alert for version {new_version}...")
    try:
        response = requests.post("https://api.pushover.net/1/messages.json", data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Pushover Launcher update: {e}")

def main():
    state = load_state()
    last_state = state.get("last_state")
    last_online_start = parse_time(state.get("last_online_start"))
    last_offline_start = parse_time(state.get("last_offline_start"))
    pushover_sent = state.get("pushover_sent", False)

    now = get_current_time()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    if ENABLE_LAUNCHER_CHECK:
        current_launcher_version = get_current_launcher_version()
        last_known_launcher = state.get("last_launcher_version")

        if current_launcher_version and current_launcher_version != last_known_launcher:
            print(f"[{timestamp} {TIMEZONE}] {Style.BRIGHT + Fore.YELLOW}NEW LAUNCHER VERSION: {current_launcher_version}{Style.RESET_ALL}")
            notify_discord_launcher_update(current_launcher_version)
            #notify_pushover_launcher_update(current_launcher_version)
            log_launcher_update(timestamp, current_launcher_version)
            state["last_launcher_version"] = current_launcher_version

    auth_online = is_port_open(AUTH_SERVER_IP, SERVER_AUTH_PORT, timeout=10)
    world_online = False

    if auth_online:
        time.sleep(10)
        world_online = world_server_sent_data(WORLD_SERVER_IP, SERVER_WORLD_PORT, timeout=10)

    online = auth_online and world_online

    if online:
        print(f"[{timestamp} {TIMEZONE}] {Style.BRIGHT + Fore.GREEN}ONLINE{Style.RESET_ALL}")
        log_status(timestamp, True, True, "ONLINE")
        if last_state != "online":
            downtime = now - last_offline_start if last_offline_start else timedelta(0)
            notify_discord_online(downtime)
            last_online_start = now
            last_state = "online"
            pushover_sent = False
        elif last_online_start and (now - last_online_start >= timedelta(minutes=5)) and not pushover_sent:
            notify_pushover_online(now - last_offline_start if last_offline_start else timedelta(0))
            pushover_sent = True
    else:
        print(f"[{timestamp} {TIMEZONE}] {Style.BRIGHT + Fore.RED}OFFLINE{Style.RESET_ALL}")
        log_status(timestamp, auth_online, world_online, "OFFLINE")
        if last_state != "offline":
            uptime = now - last_online_start if last_online_start else timedelta(0)
            notify_discord_offline(uptime)
            last_offline_start = now
            last_state = "offline"

    save_state({
        "last_state": last_state,
        "last_online_start": last_online_start.isoformat() if last_online_start else None,
        "last_offline_start": last_offline_start.isoformat() if last_offline_start else None,
        "pushover_sent": pushover_sent,
        "last_launcher_version": current_launcher_version
    })

if __name__ == "__main__":
    main()
