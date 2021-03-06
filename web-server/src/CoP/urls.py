"""CoP URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

from evolutives.views import get_preloader
from learning.views import index as learning_index

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^evaluate/', include('evolutives.urls')),
	url(r'^learning/', learning_index, name="learning"),
	url(r'^team/', TemplateView.as_view(template_name='team.html'), name="learning"),
	url(r'^get_preloader$', get_preloader, name='get_preloader'),
	url(r'^$', RedirectView.as_view(url='evaluate/')),
]
