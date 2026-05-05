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
        current_user = request.user
        user_org = request.user.org.all()
        if current_user.is_superuser:
            user_org = Organizations.objects.all()
        if Organizations.objects.filter(pk=org).exists():                       
            current_org = Organizations.objects.get(pk=org)
        else:
            return HttpResponseNotFound("Организация не найдена!")
        if not user_org.contains(current_org) and not current_user.is_superuser:
            return HttpResponse("У вас нет прав на доступ к данным!")
        tuple_data_set = oneS.check_data()
        # current_org = Organizations.objects.get(id=org)
        date_list = kernel.get_date_list()
        labels_salary = []
        labels_employees = []
        quantity_employees = 0
        salary_BU = 0
        salary_RS = 0
        for item in date_list:
            label = f'{item[0]}  {item[2]}'
            labels_salary.append(label)
            labels_employees.append(label)
        data_salary = tuple_data_set[0]
        data_employees = tuple_data_set[1]           
        end_FOT = FOT.objects.filter(organizations_id=org, month=date_list[-1][1], year=date_list[-1][0])
        end_Salary_AI = Salary_AI.objects.filter(organizations_id=org, month=date_list[-1][1], year=date_list[-1][0])        
        if len(end_FOT):
            quantity_employees = end_FOT[0].employees
            salary_BU = end_FOT[0].amount
        if len(end_Salary_AI):
            salary_RS = end_Salary_AI[0].salary
        start_period = f'{date_list[0][3]}  {date_list[0][0]}'
        end_period = f'{date_list[-1][2]}  {date_list[-1][0]}'
                        
        data_RS = giga.check_data(current_org.pk)
        
        analiz_dict = kernel.get_analize(current_org.pk)
        
        status = analiz_dict.get('status', '')
        analysis = analiz_dict.get('analysis', '')
        inconsistencies = analiz_dict.get('inconsistencies', '')
        recommendations = analiz_dict.get('recommendations', '')
        template_name = "IIapp/_main.html"

        context = {
            "title": "Главная страница",
            'user_name': current_user.phone,
            'user_org': user_org,
            "org_name": current_org.name,
            "org_pk": current_org.pk,
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
