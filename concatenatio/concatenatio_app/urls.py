from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.enter, name='auth'),
    path('reg/', views.reg, name='reg'),
    path('logout/', views.logout_view, name='logout'),
    path('item/<int:id>', views.item_template, name='item'),
    path('catalog/<str:item_type>', views.catalog_view, name='catalog'),
    path('account/', views.account, name='account'),
    path('email/', views.email, name='email'),
    path('confirm/', views.confirm, name='confirm'),
    path('basket/add/<int:item_id>', views.basket_add, name='basket_add'),
    path('basket/remove/<int:item_id>/', views.basket_remove, name='basket_remove'),
    path('basket/clear/', views.basket_clear, name='basket_clear')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

