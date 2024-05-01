import wideq
import json
from pprint import pprint

STATE_FILE = "wideq_state.json"

def authenticate(gateway):
    login_url = gateway.oauth_url()
    print("Log in here:")
    print(login_url)
    print("Then paste the URL where the browser is redirected:")
    callback_url = input()
    return wideq.Auth.from_url(gateway, callback_url)

with open(STATE_FILE) as f:
    state = json.load(f)

client = wideq.Client.load(state)
client.refresh()

if not client._auth:
    client._auth = authenticate(client.gateway)

for device in client.devices:
    print(f"{device.id}: {device.name} ({device.type.name} {device.model_id} / {device.platform_type})")

    # pprint(vars(device))
    pprint(device.data['snapshot'])

    # Control
    data = {
        "ctrlKey": "basicCtrl",
        "command": "Set",
        "dataSetList": {
            "hvState": {
                "lightBrightness": 100, # 100
                "lightOnDuration": 14, # 14
                "lightOnTime_H": 8, # 8
                "lightOnTime_M": 0,  # 0
            }
        },
    }

    client.session.device_control(device.id, data)
