"""Nursery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from NurseryApp.views import (
    NurseryLoginView,
    NurseryLogoutView,
    SignupView,
    MainPageView,
    ChildCreateView
)

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'^$', NurseryLoginView.as_view(), name='login-view'),
    url(r'^logout/$', NurseryLogoutView.as_view(), name='logout-view'),
    url(r'^signup/$', SignupView.as_view(), name='signup-view'),
    url(r'^main/$', MainPageView.as_view(), name='main-view'),
    #
    url(r'^parent/(?P<id>(\d)+)/add_child/$', ChildCreateView.as_view(), name='child-create-view')


]
