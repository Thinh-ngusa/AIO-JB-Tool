import subprocess


def command_success(command):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return result.returncode == 0

    except Exception:
        return False


def get_output(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        return (result.stdout + "\n" + result.stderr).lower()

    except Exception:
        return ""


def detect_mode():
    # NORMAL
    if command_success(["ideviceinfo"]):
        return "NORMAL"

    # RECOVERY / DFU
    output = get_output(["irecovery", "-q"])

    if not output:
        return None

    if "mode: recovery" in output or "recovery" in output:
        return "RECOVERY"

    if "mode: dfu" in output or "dfu" in output:
        return "DFU"

    # Some irecovery builds only show CPID/ECID in recovery/DFU.
    if "cpid" in output or "ecid" in output:
        return "RECOVERY"

    return None