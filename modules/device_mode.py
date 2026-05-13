import subprocess


IDEVICEINFO = r"C:\libimobiledevice\ideviceinfo.exe"
IRECOVERY = r"C:\libimobiledevice\irecovery.exe"


def run_cmd(cmd, timeout=5):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return result.stdout.strip()

    except Exception:
        return ""


def detect_mode():
    # NORMAL MODE
    normal = run_cmd([IDEVICEINFO])

    if normal:
        return "NORMAL"

    # RECOVERY MODE
    recovery = run_cmd([IRECOVERY, "-q"])

    if recovery:
        return "RECOVERY"

    return None