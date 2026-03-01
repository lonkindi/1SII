from django.shortcuts import render

from loguru import logger

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


def main_view(request):
    # if not request.user.is_authenticated:
    #     return redirect(reverse(login_view))

    template_name = 'IIapp/index.html'    

    context = {'title': 'Главная страница',
                                 
               }
    return render(request, template_name=template_name, context=context)