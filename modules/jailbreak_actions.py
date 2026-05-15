import os
import subprocess
import tempfile
import shutil

from modules.colors import (
    GREEN,
    RED,
    YELLOW,
    CYAN,
    MAGENTA,
    WHITE,
    RESET,
)

from modules.key_input import get_key

from modules.resources import (
    DOPAHIDE_IPA,
    DOPALESS_IPA,
    PALEHIDE_DIR,
    PALEHIDE_SCRIPT,
    TROLLRESTORE_BINARY,
    get_palera1n_binary,
)


def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd)
        return result.returncode == 0

    except Exception as error:
        print(f"{RED}[!] Error: {error}{RESET}")
        return False


def pause():
    input(f"\n{CYAN}Press Enter to continue...{RESET}")


def install_ipa(ipa_path):
    if not os.path.exists(ipa_path):
        print(f"{RED}[!] IPA not found: {ipa_path}{RESET}")
        return False

    temp_dir = tempfile.mkdtemp(prefix="aiojb_ipa_")
    temp_ipa = os.path.join(temp_dir, "Dopamine.ipa")

    try:
        shutil.copy2(ipa_path, temp_ipa)

        print()
        print(f"{CYAN}[*] .tipa detected. Using temporary .ipa copy.{RESET}")
        print(f"    {temp_ipa}")

        print()
        print(
            f"{CYAN}[*] Installing IPA:{RESET} "
            f"{WHITE}{temp_ipa}{RESET}"
        )

        ok = run_command([
            "ideviceinstaller",
            "install",
            temp_ipa
        ])

        if ok:
            print(f"{GREEN}[+] IPA installation completed.{RESET}")
        else:
            print(f"{RED}[!] IPA installation failed.{RESET}")

        return ok

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_palehide():
    if not os.path.exists(PALEHIDE_SCRIPT):
        print(f"{RED}[!] palehide script not found.{RESET}")
        return False

    print()
    print(f"{CYAN}[*] Running palehide bootstrap...{RESET}")

    return run_command(
        ["bash", PALEHIDE_SCRIPT],
        cwd=PALEHIDE_DIR
    )


def run_trollrestore():
    if not os.path.exists(TROLLRESTORE_BINARY):
        print(f"{RED}[!] TrollRestore binary not found.{RESET}")
        return False

    print()
    print(f"{CYAN}[*] Launching TrollRestore...{RESET}")
    print(
        f"{WHITE}"
        f"When prompted, type: Tips"
        f"{RESET}"
    )

    return run_command([TROLLRESTORE_BINARY])


def force_revert():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print(f"{RED}[!] palera1n not found.{RESET}")
        return

    print()
    print(f"{MAGENTA}Force Revert{RESET}")
    print(f"{MAGENTA}--------------{RESET}")
    print()

    print(
        f"{WHITE}"
        f"Use this when you want to remove old palera1n "
        f"(rootful/rootless) environments."
        f"{RESET}"
    )

    print()

    ok = run_command([
        palera1n,
        "--force-revert",
        "-l",
        "-v"
    ])

    print()

    if ok:
        print(
            f"{GREEN}"
            f"Done. Device may reboot again to finish force-revert."
            f"{RESET}"
        )
    else:
        print(f"{RED}[!] Force revert failed.{RESET}")

    pause()


def palera1n_rootless():
    palera1n = get_palera1n_binary()

    if not palera1n:
        print(f"{RED}[!] palera1n not found.{RESET}")
        return

    print()
    print(f"{MAGENTA}palera1n rootless{RESET}")
    print(f"{MAGENTA}------------------{RESET}")
    print()

    ok = run_command([
        palera1n,
        "-l",
        "-v"
    ])

    print()

    if ok:
        print(
            f"{GREEN}"
            f"Done. Please install Sileo/Zebra via Palera1n Loader and enjoy."
            f"{RESET}"
        )
    else:
        print(f"{RED}[!] palera1n failed.{RESET}")

    pause()


def dopamine_rootless():
    print()
    print(f"{MAGENTA}Dopamine rootless{RESET}")
    print(f"{MAGENTA}-------------------{RESET}")

    ipa_ok = install_ipa(DOPALESS_IPA)

    print()

    if ipa_ok:
        print(
            f"{GREEN}"
            f"Done. Please open TrollStore and install Dopamine."
            f"{RESET}"
        )
    else:
        print(f"{RED}[!] Dopamine installation failed.{RESET}")

    pause()


def dopamine_roothide():
    print()
    print(f"{MAGENTA}Dopamine roothide{RESET}")
    print(f"{MAGENTA}-------------------{RESET}")

    ipa_ok = install_ipa(DOPAHIDE_IPA)

    if not ipa_ok:
        print(f"{RED}[!] Dopamine roothide installation failed.{RESET}")
        pause()
        return

    print()

    palehide_ok = run_palehide()

    print()

    if palehide_ok:
        print(
            f"{GREEN}"
            f"Done. Please install Dopamine via TrollStore."
            f"{RESET}"
        )

        print(
            f"{WHITE}"
            f"You may need to run this again when your device is rebooted."
            f"{RESET}"
        )

    else:
        print(f"{RED}[!] palehide bootstrap failed.{RESET}")

    pause()


def trollrestore_dopamine():
    print()
    print(f"{MAGENTA}TrollRestore Bootstrap{RESET}")
    print(f"{MAGENTA}-----------------------{RESET}")

    ipa_ok = install_ipa(DOPAHIDE_IPA)

    if not ipa_ok:
        print(f"{RED}[!] IPA installation failed.{RESET}")
        pause()
        return

    troll_ok = run_trollrestore()

    print()

    if troll_ok:
        print(
            f"{GREEN}"
            f"Done. Open Tips to install TrollStore."
            f"{RESET}"
        )

        print(
            f"{WHITE}"
            f"Then install Dopamine normally through TrollStore."
            f"{RESET}"
        )

    else:
        print(f"{RED}[!] TrollRestore failed.{RESET}")

    pause()


def select_option():
    return get_key()


def start_jailbreak_flow(eligibility):
    group = eligibility.get("group")

    while True:
        print()
        print(f"{CYAN}Jailbreak Actions{RESET}")
        print(f"{CYAN}-----------------{RESET}")

        if group == "A":
            print(f"{CYAN}[1]{RESET} palera1n rootless")
            print(f"{CYAN}[2]{RESET} Dopamine roothide")
            print(f"{CYAN}[3]{RESET} Force Revert")
            print(f"{CYAN}[0]{RESET} Back")

            choice = select_option()

            if choice == "1":
                palera1n_rootless()

            elif choice == "2":
                dopamine_roothide()

            elif choice == "3":
                force_revert()

            elif choice == "0":
                return

        elif group == "B":
            print(f"{CYAN}[1]{RESET} palera1n rootless")
            print(f"{CYAN}[2]{RESET} Dopamine")
            print(f"{CYAN}[0]{RESET} Back")

            choice = select_option()

            if choice == "1":
                palera1n_rootless()

            elif choice == "2":
                print()
                print(f"{CYAN}[1]{RESET} Rootless")
                print(f"{CYAN}[2]{RESET} Roothide")
                print(f"{CYAN}[0]{RESET} Back")

                sub = select_option()

                if sub == "1":
                    dopamine_rootless()

                elif sub == "2":
                    trollrestore_dopamine()

            elif choice == "0":
                return

        else:
            print(f"{RED}[!] Unsupported device group.{RESET}")
            return