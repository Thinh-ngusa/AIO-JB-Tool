import subprocess


def command_success(command):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return result.returncode == 0

    except Exception:
        return False


def detect_mode():
    # NORMAL
    if command_success(["ideviceinfo"]):
        return "NORMAL"

    # RECOVERY / DFU
    try:
        result = subprocess.run(
            ["irecovery", "-q"],
            capture_output=True,
            text=True
        )

        output = result.stdout.lower()

        if "recovery" in output:
            return "RECOVERY"

        if "dfu" in output:
            return "DFU"

    except Exception:
        pass

    return None