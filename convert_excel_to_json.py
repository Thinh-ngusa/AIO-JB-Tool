import pandas as pd
import json

print("[*] Starting converter...")

EXCEL_FILE = "database/devices.xlsx"
OUTPUT_FILE = "database/devices.json"

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

print("[+] devices.json created successfully")