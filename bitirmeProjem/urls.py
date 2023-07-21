"""bitirmeProjem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, re_path
from django.views.static import serve
from urunler.views import *
from kullanici.views import *

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root':settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('urun-detay/<int:urunId>', urun, name='detay'),
    path('register/', userRegister, name='register'),
    path('login/', userLogin, name='login'),
    path('logout/',userLogout, name='logout'),
    path('olustur/', olustur, name='olustur'),
    path('sepetim/', sepetim, name='sepetim'),
    path('payment/', payment, name='payment'),
    path('result/', result, name = 'result'),
    path('success/', success, name='success'),
    path('failure', fail, name='failure'),
    path('favori_ekle/<int:urun_id>/', favori_ekle, name='favori_ekle'),
    path('favori_kaldir/<int:urun_id>/', favori_kaldir, name='favori_kaldir'),
    path('favorilerim/', favorilerim, name='favorilerim'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = 'urunler.views.view_404'
handler500 = 'urunler.views.view_500'

