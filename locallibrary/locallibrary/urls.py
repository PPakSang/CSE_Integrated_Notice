"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include #url 패턴이 일치할 때 include 안에 있는 파일에서 재 맵핑하겠다, 직관적인 구조
from django.views.generic import RedirectView # url 패턴이 일치할 때 리다이렉트 시킬 url 지정
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/',include('catalog.urls')),
    path('',RedirectView.as_view(url='/catalog/', permanent=True)),
    path('admin/clearcache/', include('clearcache.urls')),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

