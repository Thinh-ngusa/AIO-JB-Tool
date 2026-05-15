import os
import subprocess
import shutil
import platform

from modules.key_input import get_key
from modules.resources import (
    get_palera1n_binary,
    PALEHIDE_DIR,
    PALEHIDE_SCRIPT,
)

from modules.colors import (
    GREEN,
    RED,
    YELLOW,
    CYAN,
    MAGENTA,
    WHITE,
    RESET,
)


README_FILE = "readme.md"

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


def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, cwd=cwd)
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
        print(f"{RED}[!] idevicediagnostics is not installed.{RESET}")
        return

    print(f"{CYAN}[*] Rebooting device...{RESET}")

    ok = run_command(["idevicediagnostics", "restart"])

    if ok:
        print(f"{GREEN}[+] Reboot command sent.{RESET}")
    else:
        print(f"{RED}[!] Failed to reboot device.{RESET}")


def enter_recovery():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print(f"{RED}[!] palera1n is not available.{RESET}")
        return

    print(f"{CYAN}[*] Entering Recovery mode...{RESET}")

    ok = run_command([palera1n, "-E"])

    if ok:
        print(f"{GREEN}[+] Recovery command sent.{RESET}")
    else:
        print(f"{RED}[!] Failed to enter Recovery mode.{RESET}")


def exit_recovery():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print(f"{RED}[!] palera1n is not available.{RESET}")
        return

    print(f"{CYAN}[*] Exiting Recovery mode...{RESET}")

    ok = run_command([palera1n, "-n"])

    if ok:
        print(f"{GREEN}[+] Exit Recovery command sent.{RESET}")
    else:
        print(f"{RED}[!] Failed to exit Recovery mode.{RESET}")


def dfu_helper():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print(f"{RED}[!] palera1n is not available.{RESET}")
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
    print(f"{CYAN}[*] Launching palera1n DFU helper...{RESET}")

    ok = run_command([palera1n, "-D"])

    if ok:
        print(f"{GREEN}[+] DFU helper finished.{RESET}")
    else:
        print(f"{RED}[!] DFU helper failed.{RESET}")


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

    input(f"\n{CYAN}Press Enter to exit DFU helper...{RESET}")


def run_palehide():
    if not PALEHIDE_SCRIPT:
        print(f"{RED}[!] palehide script path is missing.{RESET}")
        return False

    print(f"{CYAN}[*] Running palehide bootstrap...{RESET}")

    return run_command(
        ["bash", PALEHIDE_SCRIPT],
        cwd=PALEHIDE_DIR
    )


def bootstrap_8x_dopamine(device):
    identifier = device.get("identifier")

    if identifier not in IPHONE_8_X:
        print(
            f"{YELLOW}[!] This option is intended for iPhone 8 / 8 Plus / X only.{RESET}"
        )
        return

    print()
    print(f"{MAGENTA}Bootstrap for 8/X using Dopamine{RESET}")
    print(f"{MAGENTA}--------------------------------{RESET}")
    print()
    print(f"{WHITE}This will run palehide bootstrap for Dopamine.{RESET}")
    print()

    palehide_ok = run_palehide()

    if palehide_ok:
        print()
        print(f"{GREEN}Done. Bootstrap completed.{RESET}")
        print(
            f"{WHITE}"
            f"You may need to run this again after reboot."
            f"{RESET}"
        )
    else:
        print(f"{RED}[!] palehide bootstrap failed.{RESET}")


def open_readme():
    if not os.path.exists(README_FILE):
        print(f"{RED}[!] README.md not found.{RESET}")
        return

    print(f"{CYAN}[*] Opening README...{RESET}")

    system = platform.system()

    try:
        if system == "Darwin":
            subprocess.run(["open", README_FILE])

        elif system == "Windows":
            os.startfile(README_FILE)

        else:
            subprocess.run(["xdg-open", README_FILE])

        print(f"{GREEN}[+] README opened.{RESET}")

    except Exception as error:
        print(f"{RED}[!] Failed to open README: {error}{RESET}")


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
        print(f"{CYAN}[6]{RESET} Bootstrap for 8/X using Dopamine")
        print(f"{CYAN}[7]{RESET} Open README")
        print(f"{CYAN}[0]{RESET} Back")

        choice = select_option()

        if choice == "1":
            dfu_helper()
            return "RESET"

        elif choice == "2":
            exit_dfu_help(device)
            return "RESET"

        elif choice == "3":
            enter_recovery()
            return "RESET"

        elif choice == "4":
            exit_recovery()
            return "RESET"

        elif choice == "5":
            reboot_device()
            return "RESET"

        elif choice == "6":
            bootstrap_8x_dopamine(device)
            return "RESET"

        elif choice == "7":
            open_readme()
            return "RESET"

        elif choice == "0":
            return "RESET"

        else:
            print(f"{YELLOW}[!] Invalid option.{RESET}")