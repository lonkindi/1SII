import requests

load_dotenv()

def get_access():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload={
    'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': 'f5ded670-56ff-4432-bfbd-7f366f11c443',
    'Authorization': f"Basic {os.getenv('GIGA_KEY')}"
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    access_key = response.text
    print("access_key = ", access_key)
    return access_key


def send_promt(promt):
    url = "https://gigachat.devices.sberbank.ru/api/v1/models"

    payload={promt}
    
    headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {get_access}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    response_text = response.text
    print(response_text)
    return response_text

