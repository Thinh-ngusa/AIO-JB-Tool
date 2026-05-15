import os
import subprocess
import tempfile
import shutil
import platform

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


def command_exists(command):
    return shutil.which(command) is not None


def pause():
    input(f"\n{CYAN}Press Enter to continue...{RESET}")


def select_option():
    return get_key()


def unmount_afc(mount_dir):
    system = platform.system()

    if system == "Darwin":
        subprocess.run(
            ["diskutil", "unmount", mount_dir],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.run(
            ["fusermount", "-u", mount_dir],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def send_tipa_to_device(tipa_path, output_name):
    if not os.path.exists(tipa_path):
        print(f"{RED}[!] TIPA not found: {tipa_path}{RESET}")
        return False

    if not command_exists("ifuse"):
        print(f"{RED}[!] ifuse is not installed.{RESET}")
        print(f"{WHITE}Install it first, then try again.{RESET}")
        return False

    mount_dir = tempfile.mkdtemp(prefix="aiojb_afc_")

    try:
        print()
        print(f"{CYAN}[*] Mounting device filesystem...{RESET}")

        mounted = run_command(["ifuse", mount_dir])

        if not mounted:
            print(f"{RED}[!] Failed to mount device with ifuse.{RESET}")
            return False

        target_dir = os.path.join(mount_dir, "Downloads")
        os.makedirs(target_dir, exist_ok=True)

        target_file = os.path.join(target_dir, output_name)

        print(f"{CYAN}[*] Sending TIPA to device...{RESET}")
        print(f"{WHITE}    {target_file}{RESET}")

        shutil.copy2(tipa_path, target_file)

        print()
        print(f"{GREEN}[+] TIPA sent to device successfully.{RESET}")
        print(f"{WHITE}Location on device: Downloads/{output_name}{RESET}")

        return True

    except Exception as error:
        print(f"{RED}[!] Failed to send TIPA: {error}{RESET}")
        return False

    finally:
        unmount_afc(mount_dir)
        shutil.rmtree(mount_dir, ignore_errors=True)


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
    print(f"{WHITE}When prompted, type: Tips{RESET}")

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

    sent = send_tipa_to_device(
        DOPALESS_IPA,
        "Dopaless.tipa"
    )

    print()

    if sent:
        print(
            f"{GREEN}"
            f"Done. Open TrollStore and install Dopaless.tipa from your device."
            f"{RESET}"
        )
    else:
        print(f"{RED}[!] Failed to send Dopamine rootless TIPA.{RESET}")

    pause()


def dopamine_roothide_palehide():
    print()
    print(f"{MAGENTA}Dopamine roothide{RESET}")
    print(f"{MAGENTA}-------------------{RESET}")

    sent = send_tipa_to_device(
        DOPAHIDE_IPA,
        "Dopahide.tipa"
    )

    if not sent:
        print(f"{RED}[!] Failed to send Dopamine roothide TIPA.{RESET}")
        pause()
        return

    palehide_ok = run_palehide()

    print()

    if palehide_ok:
        print(f"{GREEN}Done. Please install Dopamine via TrollStore.{RESET}")
        print(
            f"{WHITE}"
            f"You may need to run this again when your device is rebooted."
            f"{RESET}"
        )
    else:
        print(f"{RED}[!] palehide bootstrap failed.{RESET}")

    pause()


def trollrestore_dopamine_rootless():
    print()
    print(f"{MAGENTA}Dopamine rootless{RESET}")
    print(f"{MAGENTA}-------------------{RESET}")

    sent = send_tipa_to_device(
        DOPALESS_IPA,
        "Dopaless.tipa"
    )

    if not sent:
        print(f"{RED}[!] Failed to send Dopamine rootless TIPA.{RESET}")
        pause()
        return

    troll_ok = run_trollrestore()

    print()

    if troll_ok:
        print(f"{GREEN}Done. Open Tips to install TrollStore.{RESET}")
        print(f"{WHITE}Then install Dopaless.tipa using TrollStore.{RESET}")
    else:
        print(f"{RED}[!] TrollRestore failed.{RESET}")

    pause()


def trollrestore_dopamine_roothide():
    print()
    print(f"{MAGENTA}Dopamine roothide{RESET}")
    print(f"{MAGENTA}-------------------{RESET}")

    sent = send_tipa_to_device(
        DOPAHIDE_IPA,
        "Dopahide.tipa"
    )

    if not sent:
        print(f"{RED}[!] Failed to send Dopamine roothide TIPA.{RESET}")
        pause()
        return

    troll_ok = run_trollrestore()

    print()

    if troll_ok:
        print(f"{GREEN}Done. Open Tips to install TrollStore.{RESET}")
        print(f"{WHITE}Then install Dopahide.tipa using TrollStore.{RESET}")
    else:
        print(f"{RED}[!] TrollRestore failed.{RESET}")

    pause()


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
                dopamine_roothide_palehide()

            elif choice == "3":
                force_revert()

            elif choice == "0":
                return "RESET"

        elif group == "B":
            print(f"{CYAN}[1]{RESET} palera1n rootless")
            print(f"{CYAN}[2]{RESET} Dopamine")
            print(f"{CYAN}[3]{RESET} Force Revert")
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
                    trollrestore_dopamine_rootless()

                elif sub == "2":
                    trollrestore_dopamine_roothide()

            elif choice == "3":
                force_revert()

            elif choice == "0":
                return "RESET"

        elif group == "C":
            print(f"{CYAN}[1]{RESET} palera1n rootless")
            print(f"{CYAN}[2]{RESET} Dopamine roothide")
            print(f"{CYAN}[3]{RESET} Force Revert")
            print(f"{CYAN}[0]{RESET} Back")

            choice = select_option()

            if choice == "1":
                palera1n_rootless()

            elif choice == "2":
                trollrestore_dopamine_roothide()

            elif choice == "3":
                force_revert()

            elif choice == "0":
                return "RESET"

        else:
            print(f"{RED}[!] Unsupported device group.{RESET}")
            return "RESET"