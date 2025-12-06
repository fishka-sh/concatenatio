from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

# Create your views here.
def enter(request):
    return render(request, 'enter.html')