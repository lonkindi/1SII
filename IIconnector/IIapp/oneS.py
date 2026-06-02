import datetime
import calendar
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
import IIapp.kernel as kernel
from loguru import logger
from IIapp.models import FOT, Organizations, Http1S_requests


def check_data(org_id=1):
    # logger.add("log/oneS.log")
    list_FOT = []
    list_empl = []
    date_list = kernel.get_date_list()
    http1S_request = Http1S_requests.objects.filter(organizations_id=org_id, name='FOT')
    if len(http1S_request):
        resp_string = http1S_request[0].request        
        for item in date_list:
            current_FOT = FOT.objects.filter(organizations_id=org_id, year=item[0], month=item[1])
            if not (current_FOT.exists()):
                date1 = datetime.date(item[0], item[1], 1)
                date2 = datetime.date(item[0], item[1], calendar.monthrange(item[0], item[1])[1])
                resp_string = resp_string.replace('<date1>', str(date1)).replace('<date2>', str(date2))
                try:
                    response = requests.get(resp_string, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                except HTTPError as http_err:
                    logger.error(f"HTTP ошибка: {http_err}")  
                    print(f"HTTP ошибка: {http_err}")
                except ConnectionError as conn_err:
                    logger.error(f"Ошибка подключения: {conn_err}")
                    print(f"Ошибка подключения: {conn_err}")
                except Timeout as timeout_err:
                    logger.error(f"Превышено время ожидания: {timeout_err}")
                    print(f"Превышено время ожидания: {timeout_err}")
                except ValueError as json_err:  # Ошибка парсинга JSON
                    logger.error(f"Ошибка парсинга JSON: {json_err}")
                    print(f"Ошибка парсинга JSON: {json_err}")
                else:
                    if response.status_code == 200:
                        len_resp_json = len(data)
                        if len_resp_json != 0:
                            salary = 0
                            for empl in response.json():
                                salary += empl.get('Amount', 0)
                            newFOT = FOT(organizations_id=org_id, year=item[0], month=item[1], amount=salary/len_resp_json, employees=len_resp_json)
                            newFOT.save()
                            list_FOT.append(float(newFOT.amount))
                            list_empl.append(newFOT.employees)
                finally:
                    pass
            else:
                list_FOT.append(float(current_FOT[0].amount))
                list_empl.append(current_FOT[0].employees)
    return list_FOT, list_empl


def get_employees(org_id=1):
    if Organizations.objects.filter(id=org_id).exists():
        pass
