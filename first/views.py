import datetime

from django.contrib.auth.models import User
from django.shortcuts import render
from first import models
from first.forms import CalcForm


def get_menu_context():
    menu = [
        dict(title='Главная', url='/'),
        dict(title='Текущее время', url='/time'),
        dict(title='Калькулятор', url='/calc'),
        dict(title='Калькулятор (5 + 438)', url='/calc?a=5&b=438'),
        dict(title='Текущая дата', url='/date'),
        dict(title='Операции', url='/list'),
        dict(title='Авторизация', url='/login')
    ]
    return menu


# Функция-обработчик главной страницы
# request - параметр, в нём детали входящего запроса
def index_page(request):
    # Подготовка данных (в виде словаря)
    context = {}
    context['menu'] = get_menu_context()
    context['author'] = 'Ivan'
    context['creation_date'] = '27.11.2018'
    context['pages_count'] = 7

    # 1. Данные + шаблон = HTML-код
    # 2. Отправка HTML-кода на клиент
    return render(request, 'index.html', context)


def current_time(request):
    context = {}
    context['menu'] = get_menu_context()
    context['now'] = datetime.datetime.now().time()
    return render(request, 'current_time.html', context)


def calculator(request):
    context = {}
    context['menu'] = get_menu_context()
    if request.method == "GET":
        context['form'] = CalcForm()
        return render(request, 'calc.html', context)
    else:
        f = CalcForm(request.POST)
        if f.is_valid():
            a = f.data['first']
            b = f.data['second']
            c = int(a) + int(b)
            context['first'] = a
            context['second'] = b
            context['result'] = c
            operation = models.CalcOperation(date=datetime.datetime.now(), first=a, second=b, result=c)
            operation.save()
        else:
            context['form'] = f
            return render(request, 'calc.html', context)


    return render(request, 'calculator.html', context)


def date_page(request):
    context = dict()
    context['menu'] = get_menu_context()
    context['current_date'] = datetime \
        .datetime.now().date().strftime("%Y-%m-%d")
    return render(request, 'date.html', context)


def all_operations(request):
    context = dict()
    context['menu'] = get_menu_context()
    context['operations'] = models.CalcOperation.objects.all()
    return render(request, 'operations.html', context)


def login(request):
    context = dict()
    context['menu'] = get_menu_context()
    if len(request.GET) == 0:
        return render(request, "login.html", context)
    name = request.GET.get('name', '')
    surname = request.GET.get('surname', '')
    if name == '' or surname == '':
        return render(request, "login.html", context)
    u = models.User(name=name, surname=surname)
    u.save()
    print(u.id)
    request.session['id'] = u.id
    return render(request, 'index.html', context)


def me(request):
    context = dict()
    context['menu'] = get_menu_context()
    id = request.session.get('id', None)
    if id:
        u = models.User.objects.filter(id=id).first()
        context['name'] = u.name
    else:
        context['name'] = 'Anon'

    return render(request, 'me.html', context)
