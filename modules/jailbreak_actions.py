import os
import subprocess

from modules.key_input import get_key

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
        print(f"[!] Error: {error}")
        return False


def pause():
    input("\nPress Enter to return to main menu...")
    return "MAIN_MENU"


def select_option():
    print("\nSelect option: ", end="", flush=True)
    return get_key()


def print_jailbreak_notes():
    print()
    print("Notes")
    print("-----")
    print("• Make sure your device does not have a passcode enabled.")
    print("• Please back up all important data before proceeding.")
    print("• Preserving user data after jailbreak operations is not guaranteed.")
    print(
        "• If you are not sure whether your device still contains an old "
        "jailbreak environment from winra1n, checkra1n, or older palera1n "
        "setups, we highly recommend using Force-revert first."
    )


def run_palera1n_force_revert():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print("[!] palera1n is not available.")
        return

    print("[*] Running palera1n force-revert...")

    ok = run_command([palera1n, "--force-revert", "-lv"])

    if ok:
        print()
        print(
            "Done. Please reboot your device once more "
            "to complete the force-revert process."
        )

    else:
        print("[!] palera1n force-revert failed.")


def run_palera1n_rootless():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print("[!] palera1n is not available.")
        return

    print("[*] Running palera1n rootless...")

    ok = run_command([palera1n, "-lv"])

    if ok:
        print()
        print(
            "Done. Please install Sileo/Zebra "
            "via palera1n Loader and enjoy."
        )

    else:
        print("[!] palera1n failed.")


def palera1n_menu():
    while True:
        print()
        print("palera1n rootless options:")
        print()
        print("[1] Force-revert")
        print("[2] Run palera1n rootless")
        print("[0] Back")

        choice = select_option()

        if choice == "1":
            print()
            print(
                "Use this when you want to remove an old palera1n jailbreak "
                "environment, including rootful or rootless."
            )

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
            print("[!] Invalid option.")


def install_ipa(ipa_path):
    if not os.path.exists(ipa_path):
        print(f"[!] IPA not found: {ipa_path}")
        return False

    print(f"[*] Installing IPA: {ipa_path}")

    return run_command(["ideviceinstaller", "-i", ipa_path])


def run_trollrestore_tips():
    if not os.path.exists(TROLLRESTORE_BINARY):
        print(f"[!] TrollRestore binary not found: {TROLLRESTORE_BINARY}")
        return False

    print("[*] Running TrollRestore with persistence helper: Tips")

    return run_command([TROLLRESTORE_BINARY, "Tips"])


def run_palehide():
    if not os.path.exists(PALEHIDE_SCRIPT):
        print(f"[!] palehide script not found: {PALEHIDE_SCRIPT}")
        return False

    print("[*] Running palehide...")

    return run_command(
        ["bash", PALEHIDE_SCRIPT],
        cwd=PALEHIDE_DIR
    )


def dopamine_trollrestore_flow(ipa_path):
    ipa_ok = install_ipa(ipa_path)

    if not ipa_ok:
        print("[!] IPA installation failed.")
        return

    restore_ok = run_trollrestore_tips()

    if restore_ok:
        print()
        print("Done. Your device will now reboot.")
        print("After reboot, open Tips to install TrollStore.")
        print("Then install Dopamine normally via TrollStore.")

    else:
        print("[!] TrollRestore failed.")


def dopamine_palehide_flow():
    ipa_ok = install_ipa(DOPAHIDE_IPA)

    if not ipa_ok:
        print("[!] IPA installation failed.")
        return

    palehide_ok = run_palehide()

    if palehide_ok:
        print()
        print("Done. Please install Dopamine via TrollStore.")
        print(
            "You may need to run this again "
            "when your device is rebooted."
        )

    else:
        print("[!] palehide failed.")


def dopamine_menu_group_b():
    while True:
        print()
        print("Dopamine options:")
        print()
        print("[1] Rootless")
        print("[2] Roothide")
        print("[0] Back")

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
            print("[!] Invalid option.")


def jailbreak_menu_group_a():
    while True:
        print()
        print("Available options:")
        print()
        print("[1] palera1n rootless")
        print("[2] Dopamine roothide")
        print("[0] Back")

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
            print("[!] Invalid option.")


def jailbreak_menu_group_b():
    while True:
        print()
        print("Available options:")
        print()
        print("[1] palera1n rootless")
        print("[2] Dopamine")
        print("[0] Back")

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
            print("[!] Invalid option.")


def jailbreak_menu_group_c():
    while True:
        print()
        print("Available options:")
        print()
        print("[1] palera1n rootless")
        print("[2] Dopamine roothide")
        print("[0] Back")

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
            print("[!] Invalid option.")


def start_jailbreak_flow(eligibility):
    if not eligibility.get("is_supported"):
        print("[!] This device is not supported.")
        return

    group = eligibility.get("group")

    print_jailbreak_notes()

    while True:
        print()
        print("[1] Continue to jailbreak")
        print("[2] Eject device")
        print("[0] Back")

        choice = select_option()

        if choice == "1":
            if group == "A":
                result = jailbreak_menu_group_a()

            elif group == "B":
                result = jailbreak_menu_group_b()

            elif group == "C":
                result = jailbreak_menu_group_c()

            else:
                print("[!] Unknown jailbreak group.")
                return

            if result == "MAIN_MENU":
                return "RESET"

        elif choice == "2":
            run_command(["idevicepair", "unpair"])
            print("[+] Device ejected.")
            return "RESET"

        elif choice == "0":
            return "RESET"

        else:
            print("[!] Invalid option.")