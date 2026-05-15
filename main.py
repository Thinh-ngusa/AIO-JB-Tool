import time
import os

from modules.colors import (
    GREEN,
    RED,
    YELLOW,
    CYAN,
    MAGENTA,
    WHITE,
    BRIGHT,
    RESET,
)

from modules.device_mode import detect_mode
from modules.device_info import get_device_info, print_device_info
from modules.eligibility import check_eligibility, print_recommendation
from modules.jailbreak_actions import start_jailbreak_flow
from modules.utilities import utilities_menu
from modules.key_input import get_key


APP_NAME = "AIO JB Tool"
VERSION = "1.0"
TIMEOUT = 60


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print(f"{CYAN}{BRIGHT}AIO JB Tool v{VERSION}{RESET}")
    print(f"{MAGENTA}by sinszxmc{RESET}")
    print(f"{WHITE}for A11 and below devices{RESET}")
    print()


def select_option():
    return get_key()


def main_action_menu(device, eligibility):
    while True:
        print()
        print(f"{CYAN}[1]{RESET} Jailbreak")
        print(f"{CYAN}[2]{RESET} Utilities")
        print(f"{CYAN}[3]{RESET} Eject Device")
        print(f"{CYAN}[0]{RESET} Refresh")

        choice = select_option()

        if choice == "1":
            if eligibility.get("is_supported"):
                result = start_jailbreak_flow(eligibility)

                if result == "RESET":
                    return "RESET"
            else:
                print(f"{RED}[!] This device is not supported.{RESET}")

        elif choice == "2":
            utilities_menu(device)

        elif choice == "3":
            os.system("idevicepair unpair")
            print(f"{GREEN}[+] Device ejected.{RESET}")
            return "RESET"

        elif choice == "0":
            return "RESET"

        else:
            print(f"{YELLOW}[!] Invalid option.{RESET}")


def handle_normal_mode():
    device = get_device_info()

    if not device:
        print(f"{RED}[!] Could not get device info.{RESET}")
        return

    device["mode"] = "NORMAL"

    print_device_info(device)

    eligibility = check_eligibility(device)
    print_recommendation(eligibility)

    return main_action_menu(device, eligibility)


def handle_recovery_mode():
    print(f"{YELLOW}[*] Recovery mode detected.{RESET}")
    print(f"{WHITE}Device is ready for recovery operations.{RESET}")


def handle_dfu_mode():
    print(f"{MAGENTA}[*] DFU mode detected.{RESET}")
    print(f"{WHITE}Device is ready for checkm8 and restore operations.{RESET}")


def main():
    clear()
    print_header()
    print(f"{CYAN}[*] Waiting for device...{RESET}")

    start_time = time.time()
    last_mode = None
    device_shown = False

    while True:
        mode = detect_mode()

        if mode:
            if mode != last_mode:
                clear()
                print_header()

                mode_color = GREEN

                if mode == "RECOVERY":
                    mode_color = YELLOW

                elif mode == "DFU":
                    mode_color = MAGENTA

                print(f"{mode_color}[+] Device connected in {mode} mode{RESET}")
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
                    print(f"{YELLOW}[!] Unknown mode detected: {mode}{RESET}")

                last_mode = mode
                device_shown = True

        else:
            if device_shown:
                clear()
                print_header()

                print(f"{RED}[-] Device disconnected{RESET}")
                print()
                print(f"{CYAN}[*] Waiting for device...{RESET}")

                device_shown = False
                last_mode = None
                start_time = time.time()

            elif time.time() - start_time > TIMEOUT:
                print()
                print(f"{YELLOW}[!] No device detected, operation aborted.{RESET}")
                break

        time.sleep(1)


if __name__ == "__main__":
    main()