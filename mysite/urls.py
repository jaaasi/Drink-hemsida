"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from mysite.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', homepage),
    url(r'^profile/(\d+)/$', profile),
    url(r'^editEvent/(\d+)/$', editEvent),
    url(r'^eventSignUp/(\d+)/$', eventSignUp),
    url(r'^event/(\d+)/$', event),
    url(r'^createaccount/$', create_account),
    url(r'^login/$', login_view),
    url(r'^logout/$', logout_view),
    url(r'^confirmation/(?P<confirmation_code>[a-z]+)/(?P<username>[a-zA-Z0-9_-]+)/', confirmation),
    # url containing two variables for activating an account.
    url(r'^accountcreated/$', account_created),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^recept/$', recept),
    url(r'^addDrink/$', addDrink),
    url(r'^addEvent/$', addEvent),
    url(r'^deleteDrink/(?P<id>\d+)/$', deleteDrink),
    url(r'^deleteEvent/(?P<id>\d+)/$', deleteEvent),
    url(r'^promotesuper/(?P<id>\d+)/$', promotesuper),
    url(r'^demotesuper/(?P<id>\d+)/$', demotesuper),

]
