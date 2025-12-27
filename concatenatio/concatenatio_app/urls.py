from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('enter/', views.enter, name='enter'),
    path('reg/', views.reg, name='reg')
]
