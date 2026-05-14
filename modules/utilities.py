import subprocess
import shutil

from modules.key_input import get_key
from modules.resources import get_palera1n_binary


def run_command(cmd):
    try:
        result = subprocess.run(cmd)
        return result.returncode == 0

    except Exception as error:
        print(f"[!] Error: {error}")
        return False


def command_exists(command):
    return shutil.which(command) is not None


def pause():
    input("\nPress Enter to return...")


def select_option():
    print("\nSelect option: ", end="", flush=True)
    return get_key()


def reboot_device():
    if not command_exists("idevicediagnostics"):
        print("[!] idevicediagnostics is not installed.")
        return

    print("[*] Rebooting device...")

    ok = run_command(["idevicediagnostics", "restart"])

    if ok:
        print("[+] Reboot command sent.")
    else:
        print("[!] Failed to reboot device.")


def enter_recovery():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print("[!] palera1n is not available.")
        return

    print("[*] Entering Recovery mode...")

    ok = run_command([palera1n, "-E"])

    if ok:
        print("[+] Recovery command sent.")
    else:
        print("[!] Failed to enter Recovery mode.")


def exit_recovery():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print("[!] palera1n is not available.")
        return

    print("[*] Exiting Recovery mode...")

    ok = run_command([palera1n, "-n"])

    if ok:
        print("[+] Exit Recovery command sent.")
    else:
        print("[!] Failed to exit Recovery mode.")


def dfu_helper():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print("[!] palera1n is not available.")
        return

    print()
    print("DFU Helper")
    print("----------")
    print(
        "For 3rd-party software, checkm8 tools, "
        "restore utilities, and more."
    )

    print()
    print("[*] Launching palera1n DFU helper...")

    ok = run_command([palera1n, "-D"])

    if ok:
        print("[+] DFU helper finished.")
    else:
        print("[!] DFU helper failed.")


def utilities_menu():
    while True:
        print()
        print("Utilities")
        print("---------")
        print("[1] Enter DFU")
        print("[2] Enter Recovery")
        print("[3] Exit Recovery")
        print("[4] Reboot Device")
        print("[0] Back")

        choice = select_option()

        if choice == "1":
            dfu_helper()
            pause()

        elif choice == "2":
            enter_recovery()
            pause()

        elif choice == "3":
            exit_recovery()
            pause()

        elif choice == "4":
            reboot_device()
            pause()

        elif choice == "0":
            return

        else:
            print("[!] Invalid option.")