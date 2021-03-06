"""TriPereira URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
import django_eventstream
from django.contrib import admin
from django.contrib.auth import views as auth_views

from Destinos.views import home, get_followers, get_data, resultdata, chat, loginchat, messages

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url('', include('social.apps.django_app.urls', namespace='social')),  # <--
    url(r'^admin/', admin.site.urls),
    url(r'^followers/' , get_followers , name='followers' ),
    url(r'^data/' , get_data , name='data' ),
    url(r'^chat/' , chat , name='chat' ),
    url(r'^loginchat/' , loginchat , name='loginchat' ),
    url(r'^resultdata/' , resultdata , name='resultdata' ),
    url(r'^(?P<room_id>[^/]+)$', chat),
    url(r'^rooms/(?P<room_id>[^/]+)/messages/$', messages),
    url(r'^events/', include(django_eventstream.urls)),
]
