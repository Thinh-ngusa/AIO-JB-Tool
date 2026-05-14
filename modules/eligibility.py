def parse_ios(v):
    parts = []

    for x in str(v).split("."):
        if x.isdigit():
            parts.append(int(x))

    while len(parts) < 3:
        parts.append(0)

    return tuple(parts)


def ios_lte(current, target):
    return parse_ios(current) <= parse_ios(target)


def ios_lt(current, target):
    return parse_ios(current) < parse_ios(target)


IPHONE_8_X = {
    "iPhone10,1",
    "iPhone10,2",
    "iPhone10,3",
    "iPhone10,4",
    "iPhone10,5",
    "iPhone10,6",
}


IPHONE_7_BELOW = {
    "iPhone6,1",
    "iPhone6,2",
    "iPhone7,1",
    "iPhone7,2",
    "iPhone8,1",
    "iPhone8,2",
    "iPhone8,4",
    "iPhone9,1",
    "iPhone9,2",
    "iPhone9,3",
    "iPhone9,4",
}


A12_PLUS_PREFIX = {
    "iPhone11",
    "iPhone12",
    "iPhone13",
    "iPhone14",
    "iPhone15",
    "iPhone16",
    "iPhone17",
}


def is_a12_plus(identifier):
    if not identifier:
        return False

    return any(identifier.startswith(prefix) for prefix in A12_PLUS_PREFIX)


def check_eligibility(device):
    identifier = device.get("identifier")
    ios = device.get("ios")

    result = {
        "is_supported": False,
        "supported_methods": [],
        "recommendation": None,
    }

    if not identifier or not ios:
        result["recommendation"] = (
            "Sorry, we could not identify your device information."
        )
        return result

    if is_a12_plus(identifier):
        result["recommendation"] = (
            "Sorry, your device is not supported. "
            "AIO JB Tool currently supports A11 and below devices only."
        )
        return result

    # iPhone 8 / 8 Plus / X
    if identifier in IPHONE_8_X:
        result["is_supported"] = True

        if ios_lte(ios, "16.6.1"):
            result["supported_methods"] = [
                "Dopamine roothide",
                "Dopamine rootless",
                "palera1n rootless",
            ]

            result["recommendation"] = (
                "We highly recommend using Dopamine roothide "
                "for better usability and overall effectiveness."
            )

        else:
            result["supported_methods"] = [
                "Dopamine roothide",
                "palera1n rootless",
            ]

            result["recommendation"] = (
                "We recommend using palera1n rootless on this iOS version "
                "for the best stability and compatibility."
            )

        return result

    # iPhone 7 / 7 Plus and below
    if identifier in IPHONE_7_BELOW:
        result["is_supported"] = True

        if ios_lt(ios, "15.8.7"):
            result["supported_methods"] = [
                "Dopamine roothide",
                "Dopamine rootless",
                "palera1n rootless",
            ]

        else:
            result["supported_methods"] = [
                "Dopamine roothide",
                "palera1n rootless",
            ]

        result["recommendation"] = (
            "We highly recommend using Dopamine roothide "
            "for better usability and overall effectiveness."
        )

        return result

    result["recommendation"] = (
        "Sorry, your device is not supported. "
        "AIO JB Tool currently supports A11 and below devices only."
    )

    return result


def print_recommendation(result):
    print()
    print("Recommendation")
    print("--------------")

    if not result.get("is_supported"):
        print(result.get("recommendation"))
        return

    print(f"Supported: {', '.join(result.get('supported_methods', []))}")
    print(f"Recommendation: {result.get('recommendation')}")