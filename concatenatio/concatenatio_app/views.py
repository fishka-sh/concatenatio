from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from .models import Item

def index(request):
    try:
        context = { 'username' : request.user.username }
        return render(request, 'index.html', context)
    except AttributeError as e:
        return render(request, 'index.html')

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

def catalog_view(request):
    item = Item.objects.all()
    context = {
        'item_list' : item,
    }
    return render(request, 'catalog.html', context)



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