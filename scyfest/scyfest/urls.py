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

from django.conf import settings #add this
from django.conf.urls.static import static #add this

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
    path('get_ranking/', get_ranking, name='ranking_set'),
    path('scan/barra/', scan_barra, name="scan_barra"),
    path('scan/taller/', scan_taller, name="scan_taller"),
    path('scan/mercado/', scan_mercado, name="scan_mercado"),
    path('points/barra/<str:qr_text>/', points_barra, name="points_barra"),
    path('points/taller/<str:qr_text>/', points_taller, name="points_taller"),
    path('points/mercado/<str:qr_text>/', points_mercado, name="points_taller"),
    path('generate_one', generate_one_ticket, name="generate_one_ticket"),
    path('booth/<str:qr_text>/get', get_booth_points, name="get_booth_points"),
    path('booth/<str:qr_text>/add', add_booth_point, name="add_booth_point"),
    path('booth/<str:qr_text>/substract', substract_booth_point, name="substract_booth_point"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
