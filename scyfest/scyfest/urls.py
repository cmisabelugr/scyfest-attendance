"""scyfest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from attendance.views import *
from polls.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test_view, name="test_view"),
    path('t/<str:qr_text>/', ticket_home, name="ticket_home"),
    path('ticket_history/<str:qr_text>/', ticket_history, name="ticket_history"),
    path('vote/<int:poll_id>/', vote, name="vote_post"),
    path('changename/<str:qr_text>/<str:new_name>/', change_name, name="change_name"),
    path('door/scan/', door_scan, name="door_scan"),
    path('door/register/<str:qr_text>/', door_ticket, name="door_register"),
    path('ranking/', ranking_view, name='ranking_view'),
    path('get_ranking/', get_ranking, name='ranking_set')
]
