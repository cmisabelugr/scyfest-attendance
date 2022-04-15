from django.conf.urls import url

from polls import views

urlpatterns = [
    url(r'^polls_list/$', views.polls_list, name='polls_list'),
    url(r'^vote/(?P<poll_id>[0-9]+)/$', views.vote, name='vote'),
]