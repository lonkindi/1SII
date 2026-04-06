from django.shortcuts import render, redirect, reverse, get_object_or_404

import requests
import json
import datetime
from loguru import logger
from django.http import HttpResponseNotFound, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from users.forms import LoginForm
import IIapp.oneS as oneS
import IIapp.giga as giga
from IIapp.models import FOT, Organizations


class MainView(View):
    def get(self, request, org=1):       
        labels_salary = ['Апрель 2025', 'Май 2025', 'Июнь 2025', 'Июль 2025', 'Август 2025', 'Сентябрь 2025', 'Октябрь 2025', 'Ноябрь 2025', 'Декабрь 2025', 'Январь 2026', 'Февраль 2026', 'Март 2026',]
        data_salary = [1060.00, 8890.00, 18853.55, 14487.00, 14123.00, 12013.00, 13800.00, 13800.00, 19803.00, 7797.00, 13800.00, 12006.00]        
        data_RS = [87500.00, 87500.00, 87500.55, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00]
        labels_employees = ['Апрель 2025', 'Май 2025', 'Июнь 2025', 'Июль 2025', 'Август 2025', 'Сентябрь 2025', 'Октябрь 2025', 'Ноябрь 2025', 'Декабрь 2025', 'Январь 2026', 'Февраль 2026', 'Март 2026',]
        data_employees = [1, 2, 2, 3, 3, 2, 2, 2, 3, 3, 2, 1] 
        resp_dict = oneS.check_data()
        current_org = Organizations.objects.get(id=org)
        date_list = oneS.get_date_list()
        end_FOT = FOT.objects.filter(organizations_id=org, month=date_list[-1][1], year=date_list[-1][0])
        quantity_employees = end_FOT[0].employees
        start_period = f'{date_list[0][3]}  {date_list[0][0]}'
        end_period = f'{date_list[-1][2]}  {date_list[-1][0]}'
        salary_BU = 13880
        salary_RS = 87500
        recomendation = """ Для сохранения аккредитации Минцифры IT-компании в 2026 году должны соблюдать ряд требований и рекомендаций:
            - Ежегодно подтверждать статус через портал Госуслуг в установленный срок (с 7 мая по 1 июня 2025 года). Заявление подаётся только в электронном виде, бумажные варианты не принимаются. 
            - Обеспечить долю доходов от IT-деятельности не ниже установленного минимума (обычно не менее 30% от общего дохода компании). 
            - Предоставить актуальное согласие на раскрытие налоговой тайны (код 20009). Без этого документа компания не сможет подтвердить статус. Проверить наличие и срок действия согласия можно через специальный чат-бот. 
            - Соблюдать требования по средней зарплате: уровень оплаты труда в компании должен быть не ниже среднего по стране или региону для IT-отрасли. Данные предоставляются за 4-й квартал предыдущего года. 
            - Вести сайт компании с актуальной информацией, соответствующей требованиям Минцифры. 
            - Для крупных компаний — заключать соглашения с вузами для совместной работы над образовательными программами по подготовке IT-специалистов. 
            - Следить за информационной безопасностью: нарушения в этой сфере могут привести к лишению аккредитации, особенно для операторов цифровых платформ. 
            - Своевременно устранять выявленные нарушения и актуализировать все документы до 1 мая 2025 года.
            Рекомендуется заранее готовиться к процедуре подтверждения, отслеживать изменения на официальном сайте Минцифры и проверять корректность всех данных и документов.""" 
        
        req = "Я к вам пишу — чего же боле?"
        giga.count_tokens(req)
        
        template_name = "IIapp/_main.html"
        # org_name = resp_dict.get('Organization')
        context = {
            "title": "Главная страница",
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
            'recomendation': recomendation,
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
