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
from IIapp.models import FOT, Organizations, AI_promts


class MainView(View):
    def get(self, request, org=1):       
        # data_RS = [87500.00, 87500.00, 87500.55, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00, 87500.00]
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
        # print('data_salary = ', data_salary)
        # print('data_employees = ', data_employees)
        end_FOT = FOT.objects.filter(organizations_id=org, month=date_list[-1][1], year=date_list[-1][0])
        quantity_employees = end_FOT[0].employees
        start_period = f'{date_list[0][3]}  {date_list[0][0]}'
        end_period = f'{date_list[-1][2]}  {date_list[-1][0]}'
        salary_BU = end_FOT[0].amount
        
        data_RS = giga.check_data(current_org.pk)
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

        AI_promt = {
          "model": "gigachat-max",
          "messages": [
            {
              "role": "system",
              "content": "Ты — главный бухгалтер аккредитованной IT-компании. Отвечай строго в формате JSON согласно предоставленной схеме. Не добавляй комментарии и дополнительные поля."
            },
            {
              "role": "user",
              "content": "Найди официальную среднемесячную номинальную начисленную заработную плату в регионе Тюменская область по данным Росстата за февраль 2025 года. Верни только JSON с полями year, month, salary. Все значения ТОЛЬКО цифрами"
            }
          ],
          "response_format": {
            "type": "json_schema",
            "json_schema": {
              "type": "object",
              "properties": {
                "year": { "type": "number" },
                "month": { "type": "number" },
                "salary": { "type": "number" }
              },
              "required": ["year", "month", "salary"]
            }
          }
        }
        
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
