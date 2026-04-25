from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.enter, name='auth'),
    path('reg/', views.reg, name='reg'),
    # path('logout/', views.logout_view, name='logout'),
    path('item/<int:id>', views.item_template, name='item'),
    path('catalog/<str:item_type>', views.catalog_view, name='catalog'),
    path('account/', views.account, name='account'),
    path('email/', views.email, name='email')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

