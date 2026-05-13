import subprocess
import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "database", "devices.json")
IDEVICEINFO_PATH = r"C:\libimobiledevice\ideviceinfo.exe"


def run_cmd(cmd, timeout=5):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout.strip()
    except Exception:
        return ""


def load_database():
    with open(DATABASE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_ideviceinfo(output):
    info = {}

    for line in output.splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            info[key.strip()] = value.strip()

    return info


def get_device_info():
    output = run_cmd([IDEVICEINFO_PATH])

    if not output:
        return None

    raw = parse_ideviceinfo(output)
    database = load_database()

    identifier = raw.get("ProductType", "Unknown")
    db = database.get(identifier, {})

    return {
        "identifier": identifier,
        "name": db.get("name", "Unknown Device"),
        "chip": db.get("chip", "Unknown"),
        "checkm8": db.get("checkm8", False),

        "ios": raw.get("ProductVersion", "Unknown"),
        "build": raw.get("BuildVersion", "Unknown"),
        "device_name": raw.get("DeviceName", "Unknown"),
        "serial": raw.get("SerialNumber", "Unknown"),
        "udid": raw.get("UniqueDeviceID", "Unknown")
    }


def print_device_info(device):
    print("[i] Device detected")
    print()
    print(f"Device Name : {device['device_name']}")
    print(f"Name        : {device['name']}")
    print(f"Identifier  : {device['identifier']}")
    print(f"Chip        : {device['chip']}")
    print(f"checkm8     : {'Yes' if device['checkm8'] else 'No'}")
    print(f"iOS         : {device['ios']}")
    print(f"Build       : {device['build']}")
    print(f"Serial      : {device['serial']}")
    print(f"UDID        : {device['udid']}")
    print()

    if device["checkm8"]:
        print("[+] This device is supported.")
    else:
        print("[-] Sorry, your device is not supported!")