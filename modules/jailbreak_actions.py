import os
import subprocess

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
    PALEHIDE_DIR,
    PALEHIDE_SCRIPT,
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


def select_option():
    return get_key()


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


def dopamine_palehide_flow(group):
    print()
    print(f"{MAGENTA}Dopamine{RESET}")
    print(f"{MAGENTA}----------{RESET}")

    palehide_ok = run_palehide()

    print()

    if palehide_ok:
        print(f"{GREEN}Done.{RESET}")

        if group == "A":
            print(
                f"{WHITE}"
                f"You may need to run this again after reboot."
                f"{RESET}"
            )

    else:
        print(f"{RED}[!] palehide failed.{RESET}")

    pause()


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
                dopamine_palehide_flow(group)

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
                    dopamine_palehide_flow(group)

                elif sub == "2":
                    dopamine_palehide_flow(group)

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
                dopamine_palehide_flow(group)

            elif choice == "3":
                force_revert()

            elif choice == "0":
                return "RESET"

        else:
            print(f"{RED}[!] Unsupported device group.{RESET}")
            return "RESET"