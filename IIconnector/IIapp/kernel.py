import datetime
import calendar
from IIapp.models import Organizations


MONTHS_RU = {
        1: ('январь', 'января'), 2: ('февраль', 'февраля'), 3: ('март', 'марта'), 4: ('апрель', 'апреля'),
        5: ('май', 'мая'), 6: ('июнь', 'июня'), 7: ('июль', 'июля'), 8: ('август', 'августа'),
        9: ('сентябрь', 'сентября'), 10: ('октябрь', 'октября'), 11: ('ноябрь', 'ноября'), 12: ('декабрь', 'декабря')
    }


def get_date_list(org_id=1, now=datetime.datetime.now().date()):    
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
