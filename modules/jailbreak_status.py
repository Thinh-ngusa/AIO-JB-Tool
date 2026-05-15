import subprocess
import shutil


IPHONE_8_X = {
    "iPhone10,1",
    "iPhone10,2",
    "iPhone10,3",
    "iPhone10,4",
    "iPhone10,5",
    "iPhone10,6",
}


DOPAMINE_BUNDLE_IDS = [
    "com.opa334.Dopamine",
    "com.opa334.Dopamine2",
]


TROLLSTORE_BUNDLE_IDS = [
    "com.opa334.TrollStore",
]


PALERA1N_HINTS = [
    "palera1n",
    "com.palera1n.loader",
    "loader",
    "sileo",
    "org.sileo.sileo",
    "org.coolstar.SileoStore",
]


PALEHIDE_HINTS = [
    "palehide",
    "roothide",
    "bootstrap",
]


def run_command(cmd, timeout=8):
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )

        return result.stdout.strip() + "\n" + result.stderr.strip()

    except Exception:
        return ""


def check_tool_available(tool_name):
    """Check if a command-line tool is available in PATH."""
    return shutil.which(tool_name) is not None


def parse_ios(v):
    parts = []

    for x in str(v).split("."):
        if x.isdigit():
            parts.append(int(x))

    while len(parts) < 3:
        parts.append(0)

    return tuple(parts)


def ios_gt(current, target):
    return parse_ios(current) > parse_ios(target)


def has_any(text, keywords):
    if not text:
        return False

    text = text.lower()

    for keyword in keywords:
        if keyword.lower() in text:
            return True

    return False


def get_installed_apps_text():
    # Check if ideviceinstaller is available
    if not check_tool_available("ideviceinstaller"):
        return ""

    outputs = []

    commands = [
        ["ideviceinstaller", "-l"],
        ["ideviceinstaller", "-l", "-o", "list_user"],
        ["ideviceinstaller", "-l", "-o", "list_system"],
        ["ideviceinstaller", "-l", "-o", "list_all"],
    ]

    for cmd in commands:
        output = run_command(cmd)
        if output:
            outputs.append(output)

    return "\n".join(outputs)


def detect_dopamine(apps_text):
    return has_any(apps_text, DOPAMINE_BUNDLE_IDS)


def detect_trollstore(apps_text):
    return has_any(apps_text, TROLLSTORE_BUNDLE_IDS)


def detect_palera1n_apps(apps_text):
    return has_any(apps_text, PALERA1N_HINTS)


def detect_palehide_trace(apps_text):
    return has_any(apps_text, PALEHIDE_HINTS)


def detect_afc2_or_rootless_access():
    """
    Best-effort only.
    This may fail if ifuse/ssh/iproxy is not installed.
    App detection is still used as fallback.
    """
    commands = [
        ["ifuse", "--list-apps"],
    ]

    for cmd in commands:
        output = run_command(cmd, timeout=5)
        if output and "ERROR" not in output.upper():
            return True

    return False


def is_iphone_8_x(identifier):
    return identifier in IPHONE_8_X


def check_jailbreak_status(device):
    identifier = device.get("identifier")
    ios = device.get("ios")

    apps_text = get_installed_apps_text()

    dopamine_detected = detect_dopamine(apps_text)
    trollstore_detected = detect_trollstore(apps_text)
    palera1n_apps_detected = detect_palera1n_apps(apps_text)
    palehide_detected = detect_palehide_trace(apps_text)

    rootless_access = detect_afc2_or_rootless_access()

    result = {
        "status": "NOT_JAILBROKEN",
        "label": "Status: Not Jailbroken",
    }

    # palera1n applies to every supported iOS version.
    if palera1n_apps_detected or rootless_access:
        result["status"] = "JAILBROKEN"
        result["label"] = "Status: Jailbroken"
        return result

    # iPhone 8/X >16.6.1 special palehide/bootstrap case.
    if (
        identifier
        and ios
        and is_iphone_8_x(identifier)
        and ios_gt(ios, "16.6.1")
    ):
        if dopamine_detected or trollstore_detected or palehide_detected:
            result["status"] = "JAILBREAK_INACTIVE"
            result["label"] = "Status: Jailbreak detected, environment inactive"
            return result

        return result

    if dopamine_detected or trollstore_detected:
        result["status"] = "JAILBROKEN"
        result["label"] = "Status: Jailbroken"
        return result

    return result


def print_jailbreak_status(result):
    print(result.get("label", "Status: Not Jailbroken"))