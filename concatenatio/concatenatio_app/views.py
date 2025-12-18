from django.shortcuts import render

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