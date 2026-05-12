import datetime
import calendar
import requests
import IIapp.kernel as kernel
from IIapp.models import FOT, Organizations, Http1S_requests


def check_data(org_id=1):
    list_FOT = []
    list_empl = []
    date_list = kernel.get_date_list(org_id)
    http1S_request = Http1S_requests.objects.filter(organizations_id=org_id, name='FOT')
    if len(http1S_request):
        resp_string = http1S_request[0].request        
        for item in date_list:
            current_FOT = FOT.objects.filter(organizations_id=org_id, year=item[0], month=item[1])
            if not (current_FOT.exists()):
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
                        newFOT = FOT(organizations_id=org_id, year=item[0], month=item[1], amount=salary/len_resp_json, employees=len_resp_json)
                        newFOT.save()
                        list_FOT.append(float(newFOT.amount))
                        list_empl.append(newFOT.employees)
            else:
                list_FOT.append(float(current_FOT[0].amount))
                list_empl.append(current_FOT[0].employees)
    return list_FOT, list_empl


def get_employees(org_id=1):
    if Organizations.objects.filter(id=org_id).exists():
        pass
