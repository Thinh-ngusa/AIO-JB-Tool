import time
import os

from modules.device_mode import detect_mode
from modules.device_info import get_device_info, print_device_info

TIMEOUT = 60


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    clear()

    print("AIO JB Tool v0.5")
    print("----------------")
    print("[*] Waiting for device...")

    start_time = time.time()
    last_mode = None
    device_shown = False

    while True:
        mode = detect_mode()

        if mode:
            if mode != last_mode:
                clear()
                print("AIO JB Tool v0.5")
                print("----------------")
                print(f"[+] Device connected in {mode} mode")
                print()

                if mode == "NORMAL":
                    device = get_device_info()
                    if device:
                        print_device_info(device)

                last_mode = mode
                device_shown = True

        else:
            if device_shown:
                clear()
                print("AIO JB Tool v0.5")
                print("----------------")
                print("[-] Device disconnected")
                print()
                print("[*] Waiting for device...")

                device_shown = False
                last_mode = None
                start_time = time.time()

            elif time.time() - start_time > TIMEOUT:
                print()
                print("[!] No device detected, operation aborted.")
                break

        time.sleep(1)


if __name__ == "__main__":
    main()