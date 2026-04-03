import os
import requests
import uuid
import json
import IIconnector.settings as settings
from dotenv import load_dotenv
from gigachat import GigaChat

# load_dotenv()


def get_uuid():
    new_uuid = uuid.uuid4()
    return str(new_uuid)


def get_access():
    load_dotenv()
    print("GIGA_key =", os.getenv('GIGA_KEY'))
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload = {
        'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': get_uuid(),
        'Authorization': f"Basic {os.getenv('GIGA_KEY')}",
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    access_key = response.json().get('access_token')
    # print('access_key=', access_key)
    return access_key


def get_balance():
    load_dotenv()
    giga = GigaChat(
        credentials=os.getenv('GIGA_KEY'),
        ca_bundle_file=os.path.join(settings.BASE_DIR, 'russian_trusted_root_ca_pem.crt')
    )
    response = giga.get_balance()
    balance = response.balance
    for entry in balance:
        print(f"{entry.usage}: {entry.value}")
    return balance


def count_tokens(promt):
    url = "https://gigachat.devices.sberbank.ru/api/v1/tokens/count"

    payload = json.dumps({
    "model": "GigaChat",
    "input": [
    f"{promt}"
        ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {get_access()}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return response.json()[0].get('tokens')


def send_promt(promt):
    url = "https://gigachat.devices.sberbank.ru/api/v1/models"

    payload = {promt}
    
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_access}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    response_text = response.text
    print(response_text)
    return response_text

