import os
import requests
import uuid
import json
import datetime
import calendar
import IIapp.kernel as kernel
import IIconnector.settings as settings
from dotenv import load_dotenv
# from gigachat import GigaChat
import gigachat
from IIapp.models import Organizations, AI_promts, Salary_AI


# load_dotenv()


def get_uuid():
    new_uuid = uuid.uuid4()
    return str(new_uuid)


def get_access():
    load_dotenv()
    # print("GIGA_key =", os.getenv('GIGA_KEY'))
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
    giga = gigachat.GigaChat(
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
        'Authorization': f'Bearer {get_access()}'
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    response_text = response.text
    print(response_text)
    return response_text


def send_promt_sdk(promt):
    giga = gigachat.GigaChat(
        credentials=os.getenv('GIGA_KEY'),
        ca_bundle_file=os.path.join(settings.BASE_DIR, 'russian_trusted_root_ca_pem.crt'),
        scope="GIGACHAT_API_PERS",
        model="GigaChat-2-Max",
        )
   
    response = giga.chat(promt)
    
    response_content = json.dumps(response.choices[0].message.content, ensure_ascii=False, indent=2)
    response_json = json.loads(response_content)
    print('response_content  = ', response_content)
    print('type response_json =', type(response_json))
    print('response_json =',  response_json)
    return response_content


def check_data(org_id=1):    
    date_list = kernel.get_date_list(org_id)
    AI_promt = AI_promts.objects.filter(organizations_id=org_id, name='ZP_MONTH')
    promt_str = ''
    list_salary = []
    if len(AI_promt):
        promt_str = AI_promt[0].template        
        for item in date_list:
            current_Salary_AI = Salary_AI.objects.filter(organizations_id=org_id, year=item[0], month=item[1])
            if not (current_Salary_AI.exists()):
                response = ''
                promt_string = promt_str.replace('<month>', str(item[2])).replace('<year>', str(item[0]))
                # print("promt_string = ", promt_string)
                promt = json.loads(promt_string)
                
                response = send_promt_sdk(promt)
                # print("response = ", response)
                if response:
                    # print('response = ', response)
                    # print('type response = ', type(response)) 

                    dict_salary = {}
                    dict_salary = eval(json.loads(response))
                    # print('dict_salary = ', dict_salary)
                    # print('type dict_salary = ', type(dict_salary))
                    new_Salary_AI = Salary_AI(organizations_id=org_id, year=item[0], month=item[1], salary=dict_salary.get('salary', 0))
                    new_Salary_AI.save()
                    list_salary.append(float(new_Salary_AI.salary))
            else:
                list_salary.append(float(current_Salary_AI[0].salary))
    return list_salary
