"""LittleJohn URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from tickerstore.utils import init_ticker_store
from tickerstore.views import tickers_by_user, ticker_history, register_user
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='LittleJohn API')

urlpatterns = [
    url(r'^$', schema_view),
    url(r'^admin/register_user/$',register_user),
    url(r'^tickers/$',tickers_by_user),
    url(r'^tickers/(?P<ticker>\w+)/history/$',ticker_history)
]

init_ticker_store()
