from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def enter(request):
    # Если придет POST-запрос на раздел сайта /enter/
    if request.method == 'POST':
        email = request.POST.get('email')
        num = request.POST.get('num')
        password = request.POST.get('password')
    
        print('Электронная почта: ', email, '\nПароль: ', password, '\nНомер телефона: ', num, sep = '')

    return render(request, 'enter.html')

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

        return JsonResponse({'status': 'success', 'message': 'Регистрация прошла успешно'})

    return render(request, 'reg.html')