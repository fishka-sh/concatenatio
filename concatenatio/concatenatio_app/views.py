from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, EmailDigest, Item
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
import random

def index(request):
    try:
        context = { 'username' : request.user.username }
        return render(request, 'index.html', context)
    except AttributeError:
        return render(request, 'index.html')

def auth(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        # \n (терминальный n) - это перенос строки
        print('Логин: ', username, '\n', 'Пароль: ', password, sep='')

        # Авторизация: здесь ищется зарегистрированный пользователь
        user = authenticate(request, username=username, password=password)
        if user is not None: # Если пользователь есть
            print('Нашелся пользователь ', user.username)
            login(request, user)
            JsonResponse({'status' : 'success', 'message' : 'Пользователь авторизован'})
        else:
            JsonResponse({'status' : 'error', 'message' : 'Пользователь не найден'})
    return render(request, 'auth.html')

def index(request):
    try:
        item = Item.objects.all()
        context = { 'username' : request.user.username,
                    'item_list' : item } 
        return render(request, 'index.html', context)
    except AttributeError as e:
        return render(request, 'index.html')
print(all)

def enter(request):
    # Если придет POST-запрос на раздел сайта /enter/
    if request.method == 'POST':
        username = request.POST.get('email')
        num = request.POST.get('num')
        password = request.POST.get('password')

        

        user = authenticate(request, username=username, password=password, num=num)
        if user is not None:
            login(request, user)
            JsonResponse({'status' : 'success'})
        else:
            JsonResponse({'status' : 'error'})
        return render(request, 'enter.html')


def item_template(request, id):
    item = Item.objects.get(id = id)
    context = { 'title' : item.item_title,
                'image' : item.item_image,
                'price' : item.item_price,
                'description' : item.item_description,
                'quantity' : item.item_quantity

                }
    
    return render(request, 'item.html', context)

def catalog_view(request, item_type):
    if item_type == 'all':
        item = Item.objects.all()
    else:
        item = Item.objects.filter(item_type = item_type)
    context = {
        'item_list' : item,
    }
    return render(request, 'catalog.html', context, status=418)



def account(request):
    print(request.user.id)
    try:
        context = {
            'username' : request.user.username,
            'first_name' : request.user.first_name,
            'last_name' : request.user.last_name,
            'email' : request.user.email,
        }
        return render(request, 'account.html', context)
    except AttributeError:
        return HttpResponse('<h1>401 Unauthorized</h1>', status=401)
    

def reg(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        num = request.POST.get('num')
        name = request.POST.get('name')
        name2 = request.POST.get('name2')
        tg = request.POST.get('tg')
        password = request.POST.get('password')
        username = email

        print('Электронная почта: ', email, '\nПароль: ', password, '\nНомер телефона: ', num, 'Имя: ', name, 'Фамилия: ', name2, 'Тг: ', tg, sep = '')

        user = User.objects.create_user(username, email, password)

        login(request, user)

        return JsonResponse({'status' : 'success'})

    return render(request, 'reg.html')

def email(request):
    if request.method == 'POST' and request.POST.get('email'):
        
        try:
            email = request.POST.get('email')
            validate_email(email)
            print('Получилось взять имейл: ', email)
        except ValidationError:
            return JsonResponse({'status': 'error', 'message' : 'Неправильно ввёден адрес почты'}, status=400)

        send_mail(
            "Полезная рассылка",
            "Вы будете получать полезную рассылку о полезных продуктах.",
            'sofyagrajd@yandex.ru',
            [email],
            fail_silently=False,
        )

        email_digest = EmailDigest(email = email)
        email_digest.save()

        return JsonResponse({'status': 'success', 'message' : 'Отправлено'})
    return JsonResponse({'status' : 'error', 'message' : 'Метод не разрешён. Только POST.'}, status=405)