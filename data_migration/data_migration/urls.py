"""
URL configuration for data_migration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from data_file.views import UploadView, HiringsView, HiringsDepView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', UploadView.as_view()),
    path('hirings/', HiringsView.as_view()),
    path('hirings_dep/', HiringsDepView.as_view())
]
