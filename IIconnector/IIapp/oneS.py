import datetime
import calendar
import requests
from IIapp.models import FOT, Organizations, Http1S_requests


def check_data(org_id=1):
    now = datetime.datetime.now().date()
    str_date1 = '2026-03-01' #datetime.date(str_date.year - 1, str_date.month, str_date.day)
    str_date2 = '2026-03-31' #now
    date_list = []
    date1 = datetime.date(now.year - 1, now.month, 1)
    date2 = datetime.date(now.year, now.month - 1, calendar.monthrange(now.year, now.month-1)[1])
    current_date = date1
    tuple_date = (current_date.year, current_date.month)
    date_list.append(tuple_date)
    for i in range((date2 - date1).days):
        if (date1 + datetime.timedelta(days=i)).month != current_date.month:
            current_date = date1 + datetime.timedelta(days=i)
            tuple_date = (current_date.year, current_date.month)
            date_list.append(tuple_date)
    current_URL = Http1S_requests.objects.filter(organizations_id=org_id)
    row_URL = current_URL[0].request
    print(row_URL.replace("<date1>", str(date1)).replace("<date2>", str(date2)))
    print(f"{current_URL[0].request}")
    for item in date_list:
        if not (FOT.objects.filter(organizations_id=org_id, year=item[0], month=item[1]).exists()):
            date1 = datetime.date(item[0], item[1], 1)
            date2 = datetime.date(item[0], item[1], calendar.monthrange(item[0], item[1])[1])
            resp_string = f"http://178.67.206.118:8081/petr/hs/DataForAI/zp?Date1={date1}&Date2={date2}"
            response = requests.get(resp_string)
            if response.status_code == 200:
                resp_dict = response.json()[0]
                newFOT = FOT(organizations_id=org_id, year=item[0], month=item[1], amount=resp_dict.get('Amount'))
                newFOT.save()
    # response = test_data
    # Проверка статус-кода
    resp_string = f"http://178.67.206.118:8081/petr/hs/DataForAI/zp?Date1={str_date1}&Date2={str_date2}"
    response = requests.get(resp_string)
    if response.status_code == 200:
        # Вывод результата
        resp_dict = response.json()[0]
        return resp_dict
    else:
        print(f"Ошибка: {response.status_code}")
        return response.status_code
