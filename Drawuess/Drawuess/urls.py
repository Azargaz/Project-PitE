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
from .views import main_page, picture, about, extended, picture_extended, categories, random_similar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('picture/', picture, name='picture'),
    path('about/', about, name='about'),
    path('',main_page, name='main_page'),
    path('extended/', extended, name='extended'),
    path('picture_extended/', picture_extended, name='picture_extended'),
    path('categories/', categories, name='categories'),
    path('random_similar/<str:category_name>/', random_similar, name='random_similar')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)