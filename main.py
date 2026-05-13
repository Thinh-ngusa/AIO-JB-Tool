print("Hello Jailbreak")
import subprocess
import time
import os

TIMEOUT = 60  # giây


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def run_cmd(cmd):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception:
        return ""


def get_device_info():
    output = run_cmd(["ideviceinfo"])

    if not output:
        return None

    info = {}

    for line in output.splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            info[key] = value

    return info


def main():
    clear()
    print("AIO JB Tool v0.1")
    print("----------------")
    print("[*] Waiting for device...")

    start_time = time.time()

    while True:
        device = get_device_info()

        if device:
            clear()
            print("AIO JB Tool v0.1")
            print("----------------")
            print("[i] Device detected")
            print()

            print(f"Device Name : {device.get('DeviceName', 'Unknown')}")
            print(f"Product Type: {device.get('ProductType', 'Unknown')}")
            print(f"iOS Version : {device.get('ProductVersion', 'Unknown')}")
            print(f"Build       : {device.get('BuildVersion', 'Unknown')}")
            print(f"UDID        : {device.get('UniqueDeviceID', 'Unknown')}")
            print()
            print("[+] Detection completed")
            break

        if time.time() - start_time > TIMEOUT:
            print()
            print("[!] No device detected, operation aborted.")
            break

        time.sleep(1)


if __name__ == "__main__":
    main()