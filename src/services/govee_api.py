import uuid
import requests

API_KEY = "9078ff45-1908-494d-8e21-1ead6aef7bbc"
GOVEE_URL = "https://openapi.api.govee.com/router/api/v1/device/control"
HEADERS = {
    "Govee-API-Key": API_KEY,
    "Content-Type": "application/json"
}

GOVEE_IPS = {
    "192.168.1.97",
    "192.168.1.174",
    "192.168.1.175",
    "192.168.1.102",
    "192.168.1.142"
}

device_ids = [
    "60:1C:D9:36:34:39:37:1E",  # Strip 
    "05:71:5C:E7:53:68:C4:80",  # Bathroom LED 1 
    "05:43:5C:E7:53:46:7F:14",  # Bathroom LED 2 
    "05:6C:5C:E7:53:46:8D:38",  # Lamp LED 
    "03:B4:5C:E7:53:66:BF:8C"   # Closet LED 
]

Strip_Scenes = {
    "ocean":      {"id": 256,  "paramId": 255},
    "forest":     {"id": 257,  "paramId": 256},
    "rainbow":    {"id": 260,  "paramId": 259},
    "aurora":     {"id": 298,  "paramId": 297},
    "universe":   {"id": 6082, "paramId": 7991},
    "fire":       {"id": 6088, "paramId": 7997},
    "candlelight":{"id": 391,  "paramId": 427},
    "movie":      {"id": 306,  "paramId": 305},
    "party":      {"id": 290,  "paramId": 289},
    "sunrise":    {"id": 6077, "paramId": 7986}
}

LED_Scenes = {
    "rainbow": {"id": 3126, "paramId": 3276},
    "aurora": {"id": 3125, "paramId": 3275},
    "fire": {"id": 3128, "paramId": 3278},
    "candlelight": {"id": 3130, "paramId": 3280},
    "movie": {"id": 1187, "paramId": 1249},
    "party": {"id": 3131, "paramId": 3281},
    "sunrise": {"id": 3133, "paramId": 3283}
}

DIY_Scenes = {
    "Start" : 22627541
}

def requestScene(sku, device, id, paramId):
    payload = {
        "requestId": str(uuid.uuid4()),
        "payload": {
            "sku": sku,
            "device": device,
            "capability": {
                "type": "devices.capabilities.dynamic_scene",
                "instance": "lightScene",
                "value": {
                    "id": id,
                    "paramId": paramId
                }
            }
        }
    }

    requests.post(GOVEE_URL, headers=HEADERS, json=payload)

def sceneAll(sceneName):
    scene(sceneName, 0, "H6062")
    for i in range(1, 5):
        scene(sceneName, i, "H6008")

def scene(scene, device, sku):
    scenesList = LED_Scenes
    if device == 0:
        scenesList = Strip_Scenes
    requestScene(sku, device_ids[device], scenesList[scene]["id"], scenesList[scene]["paramId"])

def getSceneInfo():
    payload = {
        "requestId": str(uuid.uuid4()),
        "payload": {
            "sku": "H6062",
            "device": "60:1C:D9:36:34:39:37:1E"
        }
    }
    response = requests.post(GOVEE_URL, headers=HEADERS, json=payload)
    data = response.json()
    print(data)
