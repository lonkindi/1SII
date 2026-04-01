import datetime
import requests


def check_data():
    now = datetime.datetime.now().date()
    str_date = now + datetime.timedelta(days=1)        
    str_date1 = '2026-03-01' #datetime.date(str_date.year - 1, str_date.month, str_date.day)
    str_date2 = '2026-03-31' #now
                
    # test_data = [{'FIO': 'Волосников Никита Евгеньевич', 'DateOfBirth': '1999-07-10T00:00:00', 'Organization': 'ПЕТРОПАЛЫЧ ООО', 'Amount': 12006}]   
    resp_string = f"http://178.67.206.118:8081/petr/hs/DataForAI/zp?Date1={str_date1}&Date2={str_date2}"
    response = requests.get(resp_string)
    # response = test_data
    content_empl = {}
    # Проверка статус-кода
    if response.status_code == 200:
        # Вывод результата
        resp_dict = response.json()[0]            
        content_empl = resp_dict
    else:
        print(f"Ошибка: {response.status_code}")
