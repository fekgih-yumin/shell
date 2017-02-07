"""picture_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app import views
from app import get_images_from_flowers
from app import get_images_from_pixabay

urlpatterns = [
    url(r'^transparent',views.transparent_image,name='transparent'),
    url(r'^pixabay',get_images_from_pixabay.get_images_pixabay_com,name='pixabay'),
    url(r'^typename',views.get_typename,name='typename'),
    url(r'^get_images',views.image_database_images,name='image_database_images'),
    url(r'^flowers', get_images_from_flowers.get_images, name='get images from flowers'),
    url(r'^words',views.text_deal,name='words replace image'),
    url(r'^replace',views.image_to_deal,name='replace picyure'),
    url(r'^admin/', admin.site.urls),
]
