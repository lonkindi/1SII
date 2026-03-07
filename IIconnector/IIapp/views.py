from django.shortcuts import render

import requests
import json
from loguru import logger
from django.views import View


class MainView(View):
    def get (self, request):
        response = requests.get('http://localhost/1S_TEST/hs/employees')
        content_empl = {}
        # Проверка статус-кода
        if response.status_code == 200:
        # Вывод результата
            resp_dict = response.json()
            print(resp_dict)
            content_empl = resp_dict
        else:
            print(f"Ошибка: {response.status_code}")

        template_name = 'IIapp/index.html'    

        context = {'title': 'Главная страница',
                'content_empl': content_empl,                 
                }
        return render(request, template_name=template_name, context=context)
    

def login_view(request):
    logger.add("log/crm.log")
    if request.user.is_authenticated:
        logger.info(f'Авторизанный пользователь {request.user} на странице авторизации')
        return redirect(reverse(main_view))
    if request.method == 'POST':
        username = request.POST.get('user_login', None)
        password = request.POST.get('user_password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                logger.info(f'Успешная авторизация пользователя {user}')
                return redirect(main_view)
            else:
                logger.warning(f'Неудачная попытка авторизация пользователя {username} с паролем {password}')
        else:
            return HttpResponse('Некорректный логин или пароль!')
    template_name = 'crm/login.html'
    form = LoginForm()
    context = {'form': form,
               'information': 'Для работы в системе необходимо авторизоваться',
               }
    return render(request, template_name=template_name, context=context)
    # context = {'title': 'login_title', 'main_body': 'WELCOMMEN!'}
    # return render(request, template_name, context=context)


def logout_view(request):
    logout(request)
    return redirect(reverse(login_view))


def page_not_found_view(request, exception):
    return render(request, 'crm/404.html', status=404)

