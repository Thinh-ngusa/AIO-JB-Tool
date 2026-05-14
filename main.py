import time
import os

from modules.device_mode import detect_mode
from modules.device_info import get_device_info, print_device_info
from modules.eligibility import check_eligibility, print_recommendation
from modules.jailbreak_actions import start_jailbreak_flow
from modules.utilities import utilities_menu
from modules.key_input import get_key

from modules.resources import (
    check_resources,
    check_resource_permissions,
    print_resource_report,
)


APP_NAME = "AIO JB Tool"
VERSION = "0.5"
TIMEOUT = 60


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print(f"{APP_NAME} v{VERSION}")
    print("----------------")


def print_startup_banner():
    print_header()
    print_resource_report()
    print()


def startup_checks():
    missing = check_resources()
    permission_issues = check_resource_permissions()

    if missing or permission_issues:
        print()
        print("[!] Resource check failed. Operation aborted.")
        return False

    return True


def select_option():
    print("\nSelect option: ", end="", flush=True)
    return get_key()


def main_action_menu(eligibility):
    while True:
        print()
        print("[1] Jailbreak")
        print("[2] Utilities")
        print("[3] Eject Device")
        print("[0] Refresh")

        choice = select_option()

        if choice == "1":
            if eligibility.get("is_supported"):
                result = start_jailbreak_flow(eligibility)

                if result == "RESET":
                    return "RESET"
            else:
                print("[!] This device is not supported.")

        elif choice == "2":
            utilities_menu()

        elif choice == "3":
            os.system("idevicepair unpair")
            print("[+] Device ejected.")
            return "RESET"

        elif choice == "0":
            return "RESET"

        else:
            print("[!] Invalid option.")


def handle_normal_mode():
    device = get_device_info()

    if not device:
        print("[!] Could not get device info.")
        return

    device["mode"] = "NORMAL"

    print_device_info(device)

    eligibility = check_eligibility(device)
    print_recommendation(eligibility)

    return main_action_menu(eligibility)


def handle_recovery_mode():
    print("[*] Recovery mode detected.")
    print("[*] Available actions:")
    print("    - Exit Recovery")
    print("    - Enter DFU")


def handle_dfu_mode():
    print("[*] DFU mode detected.")
    print("[*] Device is ready for palera1n/checkm8 operations.")


def main():
    clear()
    print_startup_banner()

    if not startup_checks():
        return

    print("[*] Waiting for device...")

    start_time = time.time()
    last_mode = None
    device_shown = False

    while True:
        mode = detect_mode()

        if mode:
            if mode != last_mode:
                clear()
                print_startup_banner()

                print(f"[+] Device connected in {mode} mode")
                print()

                if mode == "NORMAL":
                    result = handle_normal_mode()

                    if result == "RESET":
                        last_mode = None
                        continue

                elif mode == "RECOVERY":
                    handle_recovery_mode()

                elif mode == "DFU":
                    handle_dfu_mode()

                else:
                    print(f"[!] Unknown mode detected: {mode}")

                last_mode = mode
                device_shown = True

        else:
            if device_shown:
                clear()
                print_startup_banner()

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