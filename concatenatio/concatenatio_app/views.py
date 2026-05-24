from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, EmailDigest, Item, EmailCode
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.conf import settings
import random
import threading

def index(request):
    try:
        item = Item.objects.all()
        context = { 'username' : request.user.username,
                    'item_list' : item } 
        return render(request, 'index.html', context)
    except AttributeError as e:
        return render(request, 'index.html')

def enter(request):
    # Если придет POST-запрос на раздел сайта /auth/
    if request.method == 'POST':
        username = request.POST.get('email')
        num = request.POST.get('num')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password, num=num)
        if user is not None:
            login(request, user)
            JsonResponse({'status' : 'success', 'message' : 'Пользователь авторизован'})
        else:
            JsonResponse({'status' : 'error', 'message' : 'Пользователь не найден'})
        return render(request, 'enter.html')
    return render(request, 'enter.html')


def item_template(request, id):
    item = Item.objects.get(id = id)
    context = { 
        'title' : item.item_title,
        'image' : item.item_image,
        'price' : item.item_price,
        'description' : item.item_description,
        'quantity' : item.item_quantity,
        'username' : request.user.username
    }
    
    return render(request, 'item.html', context)

def catalog_view(request, item_type):
    if item_type == 'all':
        item = Item.objects.all()
    else:
        item = Item.objects.filter(item_type = item_type)
    context = {
        'item_list' : item,
        'username' : request.user.username
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

def send_email_code_async(email, code):
    send_mail(
        'Продукты 24/7: код подтверждения',
        f'Ваш код подтверждения: {code}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    
def reg(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        num = request.POST.get('num')
        name = request.POST.get('firstName')
        name2 = request.POST.get('lastName')
        tg = request.POST.get('tg')
        password = request.POST.get('password')

        print('Электронная почта: ', email, '\nПароль: ', password, '\nНомер телефона: ', num, 'Имя: ', name, 'Фамилия: ', name2, 'Тг: ', tg, sep = '')

        user = User.objects.create_user(
            username = email, 
            email = email, 
            password = password,
            first_name = name,
            last_name = name2,
            is_active = False
        )

        UserProfile.objects.create(
            user = user, 
            tg = tg,
            num = num
        )

        code = str(random.randint(100000, 999999))

        EmailCode.objects.create(
            user = user,
            code = code
        )

        threading.Thread(
            target=send_email_code_async,
            args=(email, code)
        ).start()        

        request.session['pending_user_id'] = user.id
        return JsonResponse({
            'status': 'success',
            'redirect': '/confirm/'
        })
    
    if request.user.is_authenticated:
        return redirect('index')
    else:
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
            "Вы будете получать новости о новинках и скидках в магазине.",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        email_digest = EmailDigest(email = email)
        email_digest.save()

        return JsonResponse({'status': 'success', 'message' : 'Отправлено'})
    return JsonResponse({'status' : 'error', 'message' : 'Метод не разрешён. Только POST.'}, status=405)

def logout_view(request):
    logout(request)
    return redirect('index')

def confirm(request):
    if request.method == 'POST':
        code = request.POST.get('email-code')
        user_id = request.session.get('pending_user_id')

        if user_id:
            try:
                user = User.objects.get(id = user_id)
                email_code = EmailCode.objects.get(user = user, code = code)

                if email_code.code == code:
                    if not email_code.is_expired():
                        user.is_active = True
                        user.save()
                        email_code.delete()
                        login(request, user)
                        return JsonResponse({'status' : 'success', 'redirect' : '/account/'})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Срок действия кода истек'}, status=400)
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Неверный код'}, status=400)

    return render(request, 'confirm.html')

def basket_add(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, id=item_id)

        qty = int(request.GET.get('qty', 1))

        basket = request.session.get('basket', {})
        item_id_str = str(item.id)

        basket[item_id_str] = basket.get(item_id_str, 0) + qty

        request.session['basket'] = basket
        request.session.modified = True

        return redirect('basket_detail')
    else:
        return redirect('auth')

def basket_detail(request):
    if request.user.is_authenticated:
        basket = request.session.get('basket', {})

        items = Item.objects.filter(id__in=basket.keys())

        basket_items = []

        for item in items:
            quantity = basket[str(item.id)]
            total_price = item.price * quantity

            basket_items.append({
                'item': item,
                'quantity': quantity,
                'total_price': total_price
            })

        context = {
            'basket_items': basket_items,
            'username' : request.user.username
        }

        return render(request, 'basket.html', context)
    else:
        return redirect('auth')

def basket_remove(request, item_id):
    if request.user.is_authenticated:
        basket = request.session.get('basket', {})

        item_id_str = str(item_id)

        if item_id_str in basket:
            del basket[item_id_str]

        request.session['basket'] = basket
        request.session.modified = True

        return redirect('basket_detail')
    else:
        return redirect('auth')

def basket_clear(request):
    if request.user.is_authenticated:
        request.session['basket'] = {}
        request.session.modified = True

        return redirect('basket_detail')
    else:
        return redirect('auth')