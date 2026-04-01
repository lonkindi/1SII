from django.shortcuts import render, redirect, reverse, get_object_or_404

import requests
import json
import datetime
from loguru import logger
from django.http import HttpResponseNotFound, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from users.forms import LoginForm


class MainView(View):
    def get(self, request):
       

        labels = ['Апрель 2025', 'Май 2025', 'Июнь 2025', 'Июль 2025', 'Август 2025', 'Сентябрь 2025', 'Октябрь 2025', 'Ноябрь 2025', 'Декабрь 2025', 'Январь 2026', 'Февраль 2026', 'Март 2026',]
        data = [1060.00, 8890.00, 18853.55, 14487.00, 14123.00, 12013.00, 13800.00, 13800.00, 19803.00, 7797.00, 13800.00, 12006.00]        
        data_RS = [87500.00, 87500.00, 87500.55, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00]
        data_Delta = [-86440.00, -78610.00, -68647.55, -73013.00, -73377.00, -75487.00, -73700.00, -73700.00, -67697.00, -79703.00, -73700.00, -75494.00]
        
        template_name = "IIapp/_main.html"
        org_name = resp_dict.get('Organization')
        base_name = resp_dict.get('Amount')
        context = {
            "title": "Главная страница",
            "content_empl": content_empl,
            "org_name": org_name,
            "base_name": base_name,
            'labels': json.dumps(labels),
            'data': json.dumps(data),
            'data_RS': json.dumps(data_RS),
            'data_Delta': json.dumps(data_Delta),
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
