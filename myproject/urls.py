"""myproject URL Configuration

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
from django.conf.urls.static import static
from myproject import settings
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from main.views import (ActorViewSet, ExperienceViewSet, BiographyViewSet)

router = DefaultRouter()
router.register(r'actor', ActorViewSet)
router.register(r'experience', ExperienceViewSet)
router.register(r'biography', BiographyViewSet)


experience_detail = ExperienceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


biography_detail = BiographyViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^experience/(?P<pk>[0-9]+)/$',
        experience_detail, name='experience_detail'),
    url(r'^biography/(?P<pk>[0-9]+)/$',
        biography_detail, name='biography_detail'),
    url(r'^media/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('main.urls')),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    ] + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
