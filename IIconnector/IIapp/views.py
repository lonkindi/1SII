from django.shortcuts import render, redirect, reverse, get_object_or_404

import requests
import json
import datetime
from loguru import logger
from django.http import HttpResponseNotFound, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from users.forms import LoginForm
import IIapp.kernel as kernel
import IIapp.oneS as oneS
import IIapp.giga as giga
from IIapp.models import FOT, Organizations, AI_promts, Salary_AI, AI_requests


class MainView(View):
    def get(self, request, org=1):
        if not request.user.is_authenticated:
            return redirect(reverse(login_view))        
        user_name = request.user       
        tuple_data_set = oneS.check_data()
        current_org = Organizations.objects.get(id=org)
        date_list = kernel.get_date_list()
        labels_salary = []
        labels_employees = []
        for item in date_list:
            label = f'{item[0]}  {item[2]}'
            labels_salary.append(label)
            labels_employees.append(label)
        data_salary = tuple_data_set[0]
        data_employees = tuple_data_set[1]           
        end_FOT = FOT.objects.filter(organizations_id=org, month=date_list[-1][1], year=date_list[-1][0])
        end_Salary_AI = Salary_AI.objects.filter(organizations_id=org, month=date_list[-1][1], year=date_list[-1][0])
        quantity_employees = end_FOT[0].employees
        start_period = f'{date_list[0][3]}  {date_list[0][0]}'
        end_period = f'{date_list[-1][2]}  {date_list[-1][0]}'
        salary_BU = end_FOT[0].amount
        salary_RS = end_Salary_AI[0].salary
                
        data_RS = giga.check_data(current_org.pk)
        
        analiz_dict = kernel.get_analize(current_org.pk)
        
        status = analiz_dict.get('status', False)
        analysis = analiz_dict.get('analysis', '')
        inconsistencies = analiz_dict.get('inconsistencies', '')
        recommendations = analiz_dict.get('recommendations', '')

        print('type analiz_dict = ',  type(analiz_dict))
        
        # giga_ans =  "{\n  \"year\": 2025,\n  \"month\": 2,\n  \"salary\": 78431\n}"
        # dict_ans = {}
        # dict_ans = json.loads(giga_ans)
        # print('ans = ', dict_ans.get('salary', 0))
        # print('ans type= ', type(dict_ans))
        
        # AI_promt = AI_promts.objects.filter(organizations_id=1, name='ZP_MONTH')        
        # promt_string = AI_promt[0].template
        # promt = json.loads(promt_string.replace('<month>', str(date_list[0][2])).replace('<year>', str(date_list[0][0])))
        # print('promt = ',  promt)
        # print('type promt = ',  type(promt))
        
        # send_promt = giga.send_promt_sdk(promt)        
        # print('giga.send_promt = ', send_promt)
        # print('type send_promt = ', type(send_promt))
        
        template_name = "IIapp/_main.html"
        # org_name = resp_dict.get('Organization')
        context = {
            "title": "Главная страница",
            'user_name': user_name,
            "org_name": current_org.name,
            "quantity_employees": quantity_employees,
            "start_period": start_period,
            "end_period": end_period,
            'labels_salary': json.dumps(labels_salary),
            'data_salary': json.dumps(data_salary),
            'labels_employees': json.dumps(labels_employees),
            'data_employees': json.dumps(data_employees),
            'data_RS': json.dumps(data_RS),
            'salary_BU': salary_BU,
            'salary_RS': salary_RS,
            'status': status,
            'analysis': analysis,
            'inconsistencies': inconsistencies,
            'recommendations': recommendations,
        }
        return render(request, template_name=template_name, context=context)


def login_view(request):
    logger.add("log/connector.log")
    if request.user.is_authenticated:
        logger.info(f"Авторизанный пользователь {request.user} на странице входа")
        return redirect("main")
    if request.method == "POST":
        username = request.POST.get("user_login", None)
        password = request.POST.get("user_password", None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                logger.info(f"Успешная авторизация пользователя {user}")
                return redirect("main")
            else:
                logger.warning(f"Пользователь {username} не активирован")
        else:
            logger.warning(
                f"Неудачная попытка авторизация пользователя {username} с паролем {password}"
                )
            return HttpResponse("Некорректный логин или пароль!")
    template_name = "IIapp/_login.html"
    form = LoginForm()
    context = {
        "form": form,
        "title": "Вход в систему",
    }
    return render(request, template_name=template_name, context=context)


def logout_view(request):
    logout(request)
    return redirect(reverse(login_view))


def page_not_found_view(request, exception):
    return render(request, "IIapp/404.html", status=404)
