import plistlib
import subprocess

from modules.colors import (
    GREEN,
    CYAN,
    WHITE,
    RESET,
)


def get_device_info():
    try:
        result = subprocess.run(
            ["ideviceinfo", "-x"],
            capture_output=True,
            text=False
        )

        if result.returncode != 0:
            return None

        data = plistlib.loads(result.stdout)

        return {
            "name": data.get("DeviceName", "Unknown"),
            "identifier": data.get("ProductType", "Unknown"),
            "ios": data.get("ProductVersion", "Unknown"),
            "build": data.get("BuildVersion", "Unknown"),
            "udid": data.get("UniqueDeviceID", "Unknown"),
            "active_status": get_activation_status(data),
        }

    except Exception:
        return None


def get_activation_status(data):
    state = data.get("ActivationState", "")

    if state.lower() == "activated":
        return "Activated"

    if state.lower() == "unactivated":
        return "Unactivated"

    return "Unknown"


def print_device_info(device):
    print(
        f"{CYAN}Device{RESET} : "
        f"{WHITE}{device.get('name', 'Unknown')}{RESET}"
    )

    print(
        f"{CYAN}iOS{RESET}    : "
        f"{WHITE}{device.get('ios', 'Unknown')}{RESET}"
    )

    print(
        f"{CYAN}Mode{RESET}   : "
        f"{GREEN}{device.get('mode', 'Unknown')}{RESET}"
    )

    active = device.get("active_status", "Unknown")

    print(
        f"{CYAN}Active{RESET} : "
        f"{WHITE}{active}{RESET}"
    )