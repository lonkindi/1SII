import datetime
import calendar
import requests
from IIapp.models import FOT, Organizations, Http1S_requests


def get_date_list(org_id=1, now=datetime.datetime.now().date()):
    MONTHS_RU = {
        1: ('январь', 'января'), 2: ('февраль', 'февраля'), 3: ('март', 'марта'), 4: ('апрель', 'апреля'),
        5: ('май', 'мая'), 6: ('июнь', 'июня'), 7: ('июль', 'июля'), 8: ('август', 'августа'),
        9: ('сентябрь', 'сентября'), 10: ('октябрь', 'октября'), 11: ('ноябрь', 'ноября'), 12: ('декабрь', 'декабря')
    }
    if Organizations.objects.filter(id=org_id).exists():        
        now = datetime.datetime.now().date()        
        date_list = []
        date1 = datetime.date(now.year - 1, now.month, 1)
        date2 = datetime.date(now.year, now.month - 1, calendar.monthrange(now.year, now.month-1)[1])
        current_date = date1
        tuple_date = (current_date.year, current_date.month, MONTHS_RU[current_date.month][0], MONTHS_RU[current_date.month][1])
        date_list.append(tuple_date)
        for i in range((date2 - date1).days):
            if (date1 + datetime.timedelta(days=i)).month != current_date.month:
                current_date = date1 + datetime.timedelta(days=i)
                tuple_date = (current_date.year, current_date.month, MONTHS_RU[current_date.month][0], MONTHS_RU[current_date.month][1])
                date_list.append(tuple_date)
        return date_list


def check_data(org_id=1):
    str_date1 = '2026-03-01' #TEST_DATE
    str_date2 = '2026-03-31' #TEST_DATE
    date_list = get_date_list(org_id)
    http1S_request = Http1S_requests.objects.filter(organizations_id=org_id, name='FOT')
    resp_string = http1S_request[0].request
    for item in date_list:
        if not (FOT.objects.filter(organizations_id=org_id, year=item[0], month=item[1]).exists()):
            date1 = datetime.date(item[0], item[1], 1)
            date2 = datetime.date(item[0], item[1], calendar.monthrange(item[0], item[1])[1])
            resp_string = resp_string.replace('<date1>', str(date1)).replace('<date2>', str(date2))
            response = requests.get(resp_string)
            if response.status_code == 200:
                len_resp_json = len(response.json())
                if len_resp_json != 0:
                    salary = 0
                    for empl in response.json():
                        salary += empl.get('Amount', 0)
                    newFOT = FOT(organizations_id=org_id, year=item[0], month=item[1], amount=salary, employees=len_resp_json)
                    newFOT.save()
    # Проверка статус-кода
    resp_string = f"http://178.67.206.118:8081/petr/hs/DataForAI/zp?Date1={str_date1}&Date2={str_date2}"
    response = requests.get(resp_string)
    len_resp_json = len(response.json())
    if response.status_code == 200 and len_resp_json != 0:
        # Вывод результата
        resp_dict = response.json()[0]
        return resp_dict
    else:
        print(f"Ошибка: {response.status_code}")
        return response.status_code


def get_employees(org_id=1):
    if Organizations.objects.filter(id=org_id).exists():
        pass