import os
import platform
import shutil
import subprocess

from modules.colors import (
    GREEN,
    RED,
    YELLOW,
    CYAN,
    RESET,
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
TOOLS_DIR = os.path.join(RESOURCES_DIR, "tools")
SCRIPTS_DIR = os.path.join(RESOURCES_DIR, "scripts")


PALEHIDE_DIR = os.path.join(SCRIPTS_DIR, "palehide-beta7")
PALEHIDE_SCRIPT = os.path.join(PALEHIDE_DIR, "palehide.sh")

PALERA1N_MACOS = os.path.join(PALEHIDE_DIR, "palera1n-macos-universal")
PALERA1N_LINUX = os.path.join(PALEHIDE_DIR, "palera1n-linux-x86_64")

PALERA1N_INSTALL_COMMAND = (
    'sudo /bin/sh -c "$(curl -fsSL https://static.palera.in/scripts/install.sh)"'
)


REQUIRED_RESOURCES = {
    "palehide script": PALEHIDE_SCRIPT,
}


def file_exists(path):
    return os.path.exists(path)


def is_file(path):
    return os.path.isfile(path)


def is_executable(path):
    return is_file(path) and os.access(path, os.X_OK)


def check_resources():
    missing = []

    for name, path in REQUIRED_RESOURCES.items():
        if not file_exists(path):
            missing.append((name, path))

    return missing


def check_resource_permissions():
    issues = []

    executable_resources = {
        "palehide script": PALEHIDE_SCRIPT,
    }

    for name, path in executable_resources.items():
        if file_exists(path) and not is_executable(path):
            issues.append((name, path))

    return issues


def get_palera1n_binary():
    system_palera1n = shutil.which("palera1n")

    if system_palera1n:
        return system_palera1n

    system_name = platform.system()

    if system_name == "Darwin" and file_exists(PALERA1N_MACOS):
        return PALERA1N_MACOS

    if system_name == "Linux" and file_exists(PALERA1N_LINUX):
        return PALERA1N_LINUX

    return None


def is_palera1n_installed():
    return get_palera1n_binary() is not None


def print_palera1n_notice():
    binary = get_palera1n_binary()

    if binary:
        print(f"{GREEN}[+] palera1n: Available{RESET}")
        print(f"    {binary}")
        return

    print(f"{YELLOW}[!] palera1n: Not installed{RESET}")
    print(
        "    palera1n is highly recommended for the best compatibility "
        "and full functionality of this tool."
    )
    print(f"    {PALERA1N_INSTALL_COMMAND}")


def install_palera1n():
    if shutil.which("palera1n"):
        print(f"{GREEN}[+] palera1n is already installed.{RESET}")
        return True

    print(f"{CYAN}[*] Installing palera1n...{RESET}")
    print(f"{CYAN}[*] Running: {PALERA1N_INSTALL_COMMAND}{RESET}")

    try:
        result = subprocess.run(
            PALERA1N_INSTALL_COMMAND,
            shell=True,
            text=True,
        )

        if result.returncode == 0:
            print(f"{GREEN}[+] palera1n installed successfully.{RESET}")
            return True

        print(f"{RED}[!] palera1n installation failed.{RESET}")
        return False

    except Exception as error:
        print(f"{RED}[!] palera1n installation error: {error}{RESET}")
        return False