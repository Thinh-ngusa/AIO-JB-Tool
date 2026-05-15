import os
import subprocess
import shutil
import tempfile

from modules.key_input import get_key
from modules.colors import (
    GREEN,
    RED,
    YELLOW,
    CYAN,
    WHITE,
    RESET,
)

from modules.resources import (
    DOPAHIDE_IPA,
    DOPALESS_IPA,
    PALEHIDE_DIR,
    PALEHIDE_SCRIPT,
    TROLLRESTORE_BINARY,
    get_palera1n_binary,
)


def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, cwd=cwd)
        return result.returncode == 0

    except Exception as error:
        print(f"{RED}[!] Error: {error}{RESET}")
        return False


def pause():
    input(f"\n{CYAN}Press Enter to return to main menu...{RESET}")
    return "MAIN_MENU"


def select_option():
    return get_key()


def print_jailbreak_notes():
    print()
    print(f"{YELLOW}Notes{RESET}")
    print(f"{YELLOW}-----{RESET}")
    print()
    print("• Make sure your device does not have a passcode enabled.")
    print()
    print("• Please back up all important data before proceeding.")
    print()
    print("• Preserving user data after jailbreak operations is not guaranteed.")
    print()
    print(
        "• If you are not sure whether your device still contains "
        "an old jailbreak environment from winra1n, checkra1n, "
        "or older palera1n setups, we highly recommend using "
        "Force-revert first."
    )


def run_palera1n_force_revert():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print(f"{RED}[!] palera1n is not available.{RESET}")
        return

    print(f"{CYAN}[*] Running palera1n force-revert...{RESET}")

    ok = run_command([
        palera1n,
        "--force-revert",
        "-lv"
    ])

    if ok:
        print()
        print(
            f"{GREEN}"
            f"Done. Please reboot your device once more "
            f"to complete the force-revert process."
            f"{RESET}"
        )
    else:
        print(f"{RED}[!] palera1n force-revert failed.{RESET}")


def run_palera1n_rootless():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print(f"{RED}[!] palera1n is not available.{RESET}")
        return

    print(f"{CYAN}[*] Running palera1n rootless...{RESET}")

    ok = run_command([palera1n, "-lv"])

    if ok:
        print()
        print(
            f"{GREEN}"
            f"Done. Please install Sileo/Zebra "
            f"via palera1n Loader and enjoy."
            f"{RESET}"
        )
    else:
        print(f"{RED}[!] palera1n failed.{RESET}")


def palera1n_menu():
    while True:
        print()
        print(f"{CYAN}palera1n rootless options:{RESET}")
        print()
        print(f"{CYAN}[1]{RESET} Force-revert")
        print(f"{CYAN}[2]{RESET} Run palera1n rootless")
        print(f"{CYAN}[0]{RESET} Back")

        choice = select_option()

        if choice == "1":
            print()
            print(
                f"{WHITE}"
                f"Use this when you want to remove an old "
                f"palera1n jailbreak environment, including "
                f"rootful or rootless."
                f"{RESET}"
            )
            print()

            run_palera1n_force_revert()

            if pause() == "MAIN_MENU":
                return "MAIN_MENU"

        elif choice == "2":
            run_palera1n_rootless()

            if pause() == "MAIN_MENU":
                return "MAIN_MENU"

        elif choice == "0":
            return

        else:
            print(f"{YELLOW}[!] Invalid option.{RESET}")


def prepare_ipa_for_install(ipa_path):
    """
    ideviceinstaller expects .ipa.
    Some packages are .tipa for TrollStore, but structurally they are often IPA files.
    This creates a temporary .ipa copy when needed.
    """

    if ipa_path.lower().endswith(".ipa"):
        return ipa_path, None

    if ipa_path.lower().endswith(".tipa"):
        temp_dir = tempfile.mkdtemp(prefix="aiojb_ipa_")
        temp_ipa = os.path.join(
            temp_dir,
            os.path.basename(ipa_path)[:-5] + ".ipa"
        )

        shutil.copy2(ipa_path, temp_ipa)

        print(f"{YELLOW}[*] .tipa detected. Using temporary .ipa copy.{RESET}")
        print(f"{WHITE}    {temp_ipa}{RESET}")

        return temp_ipa, temp_dir

    return ipa_path, None


def cleanup_temp_dir(temp_dir):
    if temp_dir and os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)


def install_ipa(ipa_path):
    if not os.path.exists(ipa_path):
        print(f"{RED}[!] IPA not found: {ipa_path}{RESET}")
        return False

    if not shutil.which("ideviceinstaller"):
        print()
        print(f"{RED}[!] ideviceinstaller is not installed or not found in PATH.{RESET}")
        print()
        print(f"{YELLOW}[*] Install it with:{RESET}")
        print(f"{WHITE}    brew install --HEAD ideviceinstaller{RESET}")
        print()
        print(f"{YELLOW}[*] If that fails, try:{RESET}")
        print(f"{WHITE}    brew tap libimobiledevice/homebrew-libimobiledevice{RESET}")
        print(f"{WHITE}    brew install ideviceinstaller{RESET}")
        return False

    install_path, temp_dir = prepare_ipa_for_install(ipa_path)

    print(
        f"{CYAN}[*] Installing IPA:{RESET} "
        f"{WHITE}{install_path}{RESET}"
    )

    try:
        result = subprocess.run(
            ["ideviceinstaller", "-i", install_path],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            print(f"{GREEN}[+] IPA installed successfully.{RESET}")
            return True

        print()
        print(f"{RED}[!] IPA installation failed.{RESET}")

        if result.stderr:
            print()
            print(f"{YELLOW}Error details:{RESET}")
            print(f"{WHITE}{result.stderr.strip()}{RESET}")

        if result.stdout:
            print()
            print(f"{YELLOW}Output:{RESET}")
            print(f"{WHITE}{result.stdout.strip()}{RESET}")

        print()
        print(f"{YELLOW}[*] Troubleshooting:{RESET}")
        print(f"{WHITE}1. Make sure the device is connected and trusted.{RESET}")
        print(f"{WHITE}2. Unlock the device before installing.{RESET}")
        print(f"{WHITE}3. Make sure the device is in normal mode.{RESET}")
        print(f"{WHITE}4. If this is a .tipa, it may require TrollStore.{RESET}")
        print(f"{WHITE}5. Reinstall ideviceinstaller if needed:{RESET}")
        print(f"{WHITE}   brew install --HEAD ideviceinstaller{RESET}")

        return False

    except subprocess.TimeoutExpired:
        print()
        print(f"{RED}[!] Installation timed out.{RESET}")
        print(f"{YELLOW}[*] Try again or check device connection.{RESET}")
        return False

    except Exception as error:
        print()
        print(f"{RED}[!] Unexpected error: {error}{RESET}")
        return False

    finally:
        cleanup_temp_dir(temp_dir)


def run_trollrestore_tips():
    if not os.path.exists(TROLLRESTORE_BINARY):
        print(
            f"{RED}"
            f"[!] TrollRestore binary not found."
            f"{RESET}"
        )
        return False

    print(
        f"{CYAN}"
        f"[*] Running TrollRestore with "
        f"persistence helper: Tips"
        f"{RESET}"
    )

    return run_command([
        TROLLRESTORE_BINARY,
        "Tips"
    ])


def run_palehide():
    if not os.path.exists(PALEHIDE_SCRIPT):
        print(f"{RED}[!] palehide script not found.{RESET}")
        return False

    print(f"{CYAN}[*] Running palehide...{RESET}")

    return run_command(
        ["bash", PALEHIDE_SCRIPT],
        cwd=PALEHIDE_DIR
    )


def dopamine_trollrestore_flow(ipa_path):
    ipa_ok = install_ipa(ipa_path)

    if not ipa_ok:
        print(f"{RED}[!] IPA installation failed.{RESET}")
        return

    restore_ok = run_trollrestore_tips()

    if restore_ok:
        print()
        print(
            f"{GREEN}"
            f"Done. Your device will now reboot."
            f"{RESET}"
        )
        print(
            f"{WHITE}"
            f"After reboot, open Tips to install TrollStore."
            f"{RESET}"
        )
        print(
            f"{WHITE}"
            f"Then install Dopamine normally via TrollStore."
            f"{RESET}"
        )
    else:
        print(f"{RED}[!] TrollRestore failed.{RESET}")


def dopamine_palehide_flow():
    ipa_ok = install_ipa(DOPAHIDE_IPA)

    if not ipa_ok:
        print(f"{RED}[!] IPA installation failed.{RESET}")
        return

    palehide_ok = run_palehide()

    if palehide_ok:
        print()
        print(
            f"{GREEN}"
            f"Done. Please install Dopamine via TrollStore."
            f"{RESET}"
        )
        print(
            f"{WHITE}"
            f"You may need to run this again "
            f"when your device is rebooted."
            f"{RESET}"
        )
    else:
        print(f"{RED}[!] palehide failed.{RESET}")


def dopamine_menu_group_b():
    while True:
        print()
        print(f"{CYAN}Dopamine options:{RESET}")
        print()
        print(f"{CYAN}[1]{RESET} Rootless")
        print(f"{CYAN}[2]{RESET} Roothide")
        print(f"{CYAN}[0]{RESET} Back")

        choice = select_option()

        if choice == "1":
            dopamine_trollrestore_flow(DOPALESS_IPA)

            if pause() == "MAIN_MENU":
                return "MAIN_MENU"

        elif choice == "2":
            dopamine_trollrestore_flow(DOPAHIDE_IPA)

            if pause() == "MAIN_MENU":
                return "MAIN_MENU"

        elif choice == "0":
            return

        else:
            print(f"{YELLOW}[!] Invalid option.{RESET}")


def jailbreak_menu_group_a():
    while True:
        print()
        print(f"{CYAN}Available options:{RESET}")
        print()
        print(f"{CYAN}[1]{RESET} palera1n rootless")
        print(f"{CYAN}[2]{RESET} Dopamine roothide")
        print(f"{CYAN}[0]{RESET} Back")

        choice = select_option()

        if choice == "1":
            result = palera1n_menu()

            if result == "MAIN_MENU":
                return "MAIN_MENU"

        elif choice == "2":
            dopamine_palehide_flow()

            if pause() == "MAIN_MENU":
                return "MAIN_MENU"

        elif choice == "0":
            return

        else:
            print(f"{YELLOW}[!] Invalid option.{RESET}")


def jailbreak_menu_group_b():
    while True:
        print()
        print(f"{CYAN}Available options:{RESET}")
        print()
        print(f"{CYAN}[1]{RESET} palera1n rootless")
        print(f"{CYAN}[2]{RESET} Dopamine")
        print(f"{CYAN}[0]{RESET} Back")

        choice = select_option()

        if choice == "1":
            result = palera1n_menu()

            if result == "MAIN_MENU":
                return "MAIN_MENU"

        elif choice == "2":
            result = dopamine_menu_group_b()

            if result == "MAIN_MENU":
                return "MAIN_MENU"

        elif choice == "0":
            return

        else:
            print(f"{YELLOW}[!] Invalid option.{RESET}")


def jailbreak_menu_group_c():
    while True:
        print()
        print(f"{CYAN}Available options:{RESET}")
        print()
        print(f"{CYAN}[1]{RESET} palera1n rootless")
        print(f"{CYAN}[2]{RESET} Dopamine roothide")
        print(f"{CYAN}[0]{RESET} Back")

        choice = select_option()

        if choice == "1":
            result = palera1n_menu()

            if result == "MAIN_MENU":
                return "MAIN_MENU"

        elif choice == "2":
            dopamine_trollrestore_flow(DOPAHIDE_IPA)

            if pause() == "MAIN_MENU":
                return "MAIN_MENU"

        elif choice == "0":
            return

        else:
            print(f"{YELLOW}[!] Invalid option.{RESET}")


def start_jailbreak_flow(eligibility):
    if not eligibility.get("is_supported"):
        print(f"{RED}[!] This device is not supported.{RESET}")
        return

    group = eligibility.get("group")

    print_jailbreak_notes()

    while True:
        print()
        print(f"{CYAN}[1]{RESET} Continue to jailbreak")
        print(f"{CYAN}[0]{RESET} Back")

        choice = select_option()

        if choice == "1":
            if group == "A":
                result = jailbreak_menu_group_a()

            elif group == "B":
                result = jailbreak_menu_group_b()

            elif group == "C":
                result = jailbreak_menu_group_c()

            else:
                print(f"{RED}[!] Unknown jailbreak group.{RESET}")
                return

            if result == "MAIN_MENU":
                return "RESET"

        elif choice == "0":
            return "RESET"

        else:
            print(f"{YELLOW}[!] Invalid option.{RESET}")