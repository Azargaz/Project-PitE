"""Drawuess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import main_page, about, extended, guess_image, get_random_similars, categories

urlpatterns = [
    path('admin/', admin.site.urls),
    path('guess_image/', guess_image, name='guess_image'),
    path('about/', about, name='about'),
    path('', main_page, name='main_page'),
    path('extended/', extended, name='extended'),
    path('get_random_similars/<int:count>/', get_random_similars, name='picture_extended'),
    path('categories/', categories, name='categories')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)