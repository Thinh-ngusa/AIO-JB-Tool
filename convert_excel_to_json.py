"""
Convert Excel device database to JSON format.

Note: This script requires pandas. Install with:
    pip install pandas

Usage:
    python3 convert_excel_to_json.py
"""

import json
import os
import sys


def main():
    try:
        import pandas as pd
    except ImportError:
        print("[!] Error: pandas is not installed.")
        print("[*] Install with: pip install pandas")
        sys.exit(1)

    EXCEL_FILE = "database/devices.xlsx"
    OUTPUT_FILE = "database/devices.json"

    if not os.path.exists(EXCEL_FILE):
        print(f"[!] Error: {EXCEL_FILE} not found.")
        sys.exit(1)

    print("[*] Starting converter...")

    try:
        df = pd.read_excel(EXCEL_FILE)
        devices = {}

        for _, row in df.iterrows():
            identifier = str(row["identifier"]).strip()

            devices[identifier] = {
                "name": str(row["name"]).strip(),
                "chip": str(row["chip"]).strip(),
                "checkm8": bool(row["checkm8"])
            }

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=2, ensure_ascii=False)

        print(f"[+] {OUTPUT_FILE} created successfully")

    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()