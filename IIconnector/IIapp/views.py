from django.shortcuts import render, redirect, reverse, get_object_or_404

import requests
import json
from loguru import logger
from django.http import HttpResponseNotFound, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from users.forms import LoginForm


class MainView(View):
    def get(self, request):
        response = requests.get("http://localhost/1S_TEST/hs/employees")
        content_empl = {}
        # Проверка статус-кода
        if response.status_code == 200:
            # Вывод результата
            resp_dict = response.json()
            print(resp_dict)
            content_empl = resp_dict
        else:
            print(f"Ошибка: {response.status_code}")

        template_name = "IIapp/_main.html"
        org_name = "ООО «Петропалыч»"
        base_name = "1С:Бухгалтерия (ПРОФ)"
        context = {
            "title": "Главная страница",
            "content_empl": content_empl,
            "org_name": org_name,
            "base_name": base_name,
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
