"""jira URL Configuration

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
from dashing.utils import router
from .widgets import *
from dashboard import urls
router.register(CustomWidget, 'custom_widget', eg_kwargs_param="[A-Za-z0-9_-]+")
router.register(OpenIssuesWidget, 'open_issues', eg_kwargs_param="[A-Za-z0-9_-]+")
router.register(ClosedIssuesWidget, 'close_issues', eg_kwargs_param="[A-Za-z0-9_-]+")
router.register(CompletionGraph, 'completion', eg_kwargs_param="[A-Za-z0-9_-]+")

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^dashing/', include(router.urls)),
	url(r'^custom/', include(urls)),
]
