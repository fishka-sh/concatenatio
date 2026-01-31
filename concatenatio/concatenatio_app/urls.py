from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('enter/', views.enter, name='enter'),
    path('reg/', views.reg, name='reg'),
    path('item/<int:id>', views.item_template, name='item'),
    path('catalog/', views.catalog_view, name='catalog')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

