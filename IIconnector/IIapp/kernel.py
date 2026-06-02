import datetime
import calendar
import json
import IIapp.giga as giga
from loguru import logger
from IIapp.models import Organizations, Salary_AI, FOT, AI_requests, AI_promts


MONTHS_RU = {
        1: ('январь', 'января'), 2: ('февраль', 'февраля'), 3: ('март', 'марта'), 4: ('апрель', 'апреля'),
        5: ('май', 'мая'), 6: ('июнь', 'июня'), 7: ('июль', 'июля'), 8: ('август', 'августа'),
        9: ('сентябрь', 'сентября'), 10: ('октябрь', 'октября'), 11: ('ноябрь', 'ноября'), 12: ('декабрь', 'декабря')
    }


def get_date_list():
    now = datetime.datetime.now().date()        
    date_list = []
    date1 = datetime.date(now.year - 1, now.month, 1)
    date2 = datetime.date(now.year, now.month - 1, calendar.monthrange(now.year, now.month-1)[1])
    current_date = date1
    logger.info(f"get_date_list: {date1, date2}")
    tuple_date = (current_date.year, current_date.month, MONTHS_RU[current_date.month][0], MONTHS_RU[current_date.month][1])
    date_list.append(tuple_date)
    for i in range((date2 - date1).days):
        if (date1 + datetime.timedelta(days=i)).month != current_date.month:
            current_date = date1 + datetime.timedelta(days=i)
            tuple_date = (current_date.year, current_date.month, MONTHS_RU[current_date.month][0], MONTHS_RU[current_date.month][1])
            date_list.append(tuple_date)
    return date_list


def get_data(org_id=1, now=datetime.datetime.now().date()):
    if Organizations.objects.filter(id=org_id).exists():
        date_list = get_date_list()
        data_string = ''
        for item in date_list:
            current_Salary_AI = Salary_AI.objects.filter(organizations_id=org_id, year=item[0], month=item[1])
            current_FOT = FOT.objects.filter(organizations_id=org_id, year=item[0], month=item[1])
            if len(current_FOT):
                data_string += f' {item[2]} {item[0]} (средняя зарплата по данным Росстата: {current_Salary_AI[0].salary} руб., начисленная зарплата: {current_FOT[0].amount} руб., численность сотрудников: {current_FOT[0].employees}),'            
    return data_string[:-1]


def get_analize(org_id=1, now=datetime.datetime.now().date()):
    analize_dict = {}
    if Organizations.objects.filter(id=org_id).exists():
        current_analize = AI_requests.objects.filter(organizations_id=org_id).filter(date_request__gt=datetime.date(now.year, now.month - 1, calendar.monthrange(now.year, now.month-1)[1]))
        if len(current_analize) == 0:
            AI_promt = AI_promts.objects.filter(organizations_id=org_id, name='ANALIZ')
            if len(AI_promt):    
                promt_str = AI_promt[0].template            
                promt_data_str = get_data(org_id)
                promt_string = promt_str.replace('<data>', promt_data_str)
                promt_dict = json.loads(promt_string)
                response_content = giga.send_promt_sdk(promt_dict)
                new_analize = AI_requests(organizations_id=org_id, promt_name='ANALIZ', request=promt_string, response=response_content, date_request=datetime.datetime.now().date())
                new_analize.save()
                current_analize = new_analize
        else:
            current_analize = current_analize[0]            
            analize_dict = eval(json.loads(current_analize.response))        
    return analize_dict
