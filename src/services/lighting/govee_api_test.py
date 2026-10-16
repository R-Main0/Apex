import os
import requests
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GOVEE_API_KEY")
if not api_key:
    raise RuntimeError("GOVEE_API_KEY missing")

url = "https://openapi.api.govee.com/router/api/v1/user/devices"

response = requests.get(
    url,
    headers={
        "Govee-API-Key": api_key,
        "Content-Type": "application/json",
    },
    timeout=15,
)

print("HTTP:", response.status_code)
print("Body:", response.text)

if response.ok:
    body = response.json()
    data = body.get("data")

    if isinstance(data, list):
        devices = data
    elif isinstance(data, dict):
        devices = data.get("devices", [])
    else:
        devices = []

    print(f"\nFound {len(devices)} devices")

    for device in devices:
        print(
            f"Name: {device.get('deviceName', '(unnamed)')} | "
            f"ID: {device.get('device')} | "
            f"Model: {device.get('sku', device.get('model'))}"
        )