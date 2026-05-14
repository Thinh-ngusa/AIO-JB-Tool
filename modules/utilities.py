import subprocess
import shutil

from modules.key_input import get_key
from modules.resources import get_palera1n_binary

from modules.colors import (
    GREEN,
    RED,
    YELLOW,
    CYAN,
    MAGENTA,
    WHITE,
    RESET,
)


IPHONE_8_X = {
    "iPhone10,1",
    "iPhone10,2",
    "iPhone10,3",
    "iPhone10,4",
    "iPhone10,5",
    "iPhone10,6",
}

IPHONE_7 = {
    "iPhone9,1",
    "iPhone9,2",
    "iPhone9,3",
    "iPhone9,4",
}


def run_command(cmd):
    try:
        result = subprocess.run(cmd)
        return result.returncode == 0

    except Exception as error:
        print(f"{RED}[!] Error: {error}{RESET}")
        return False


def command_exists(command):
    return shutil.which(command) is not None


def pause():
    input(f"\n{CYAN}Press Enter to return...{RESET}")


def select_option():
    return get_key()


def reboot_device():
    if not command_exists("idevicediagnostics"):
        print(
            f"{RED}[!] idevicediagnostics is not installed.{RESET}"
        )

        return

    print(
        f"{CYAN}[*] Rebooting device...{RESET}"
    )

    ok = run_command(["idevicediagnostics", "restart"])

    if ok:
        print(
            f"{GREEN}[+] Reboot command sent.{RESET}"
        )

    else:
        print(
            f"{RED}[!] Failed to reboot device.{RESET}"
        )


def enter_recovery():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print(
            f"{RED}[!] palera1n is not available.{RESET}"
        )

        return

    print(
        f"{CYAN}[*] Entering Recovery mode...{RESET}"
    )

    ok = run_command([palera1n, "-E"])

    if ok:
        print(
            f"{GREEN}[+] Recovery command sent.{RESET}"
        )

    else:
        print(
            f"{RED}[!] Failed to enter Recovery mode.{RESET}"
        )


def exit_recovery():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print(
            f"{RED}[!] palera1n is not available.{RESET}"
        )

        return

    print(
        f"{CYAN}[*] Exiting Recovery mode...{RESET}"
    )

    ok = run_command([palera1n, "-n"])

    if ok:
        print(
            f"{GREEN}[+] Exit Recovery command sent.{RESET}"
        )

    else:
        print(
            f"{RED}[!] Failed to exit Recovery mode.{RESET}"
        )


def dfu_helper():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print(
            f"{RED}[!] palera1n is not available.{RESET}"
        )

        return

    print()

    print(f"{MAGENTA}DFU Helper{RESET}")
    print(f"{MAGENTA}----------{RESET}")

    print(
        f"{WHITE}"
        f"For 3rd-party software, checkm8 tools, "
        f"restore utilities, and more."
        f"{RESET}"
    )

    print()

    print(
        f"{CYAN}[*] Launching palera1n DFU helper...{RESET}"
    )

    ok = run_command([palera1n, "-D"])

    if ok:
        print(
            f"{GREEN}[+] DFU helper finished.{RESET}"
        )

    else:
        print(
            f"{RED}[!] DFU helper failed.{RESET}"
        )


def exit_dfu_help(device):
    identifier = device.get("identifier")

    print()

    print(f"{MAGENTA}Exit DFU{RESET}")
    print(f"{MAGENTA}--------{RESET}")

    print()

    if identifier in IPHONE_8_X:
        print("1. Press Volume Up quickly.")
        print("2. Press Volume Down quickly.")
        print("3. Hold Side Button until the Apple logo appears.")

    elif identifier in IPHONE_7:
        print("Hold Power + Volume Down")
        print("until the Apple logo appears.")

    else:
        print("Hold Power + Home")
        print("until the Apple logo appears.")

    input(
        f"\n{CYAN}Press Enter to exit DFU helper...{RESET}"
    )


def utilities_menu(device):
    while True:
        print()

        print(f"{CYAN}Utilities{RESET}")
        print(f"{CYAN}---------{RESET}")

        print(f"{CYAN}[1]{RESET} Enter DFU")
        print(f"{CYAN}[2]{RESET} Exit DFU Help")
        print(f"{CYAN}[3]{RESET} Enter Recovery")
        print(f"{CYAN}[4]{RESET} Exit Recovery")
        print(f"{CYAN}[5]{RESET} Reboot Device")
        print(f"{CYAN}[0]{RESET} Back")

        choice = select_option()

        if choice == "1":
            dfu_helper()
            pause()

        elif choice == "2":
            exit_dfu_help(device)

        elif choice == "3":
            enter_recovery()
            pause()

        elif choice == "4":
            exit_recovery()
            pause()

        elif choice == "5":
            reboot_device()
            pause()

        elif choice == "0":
            return

        else:
            print(
                f"{YELLOW}[!] Invalid option.{RESET}"
            )