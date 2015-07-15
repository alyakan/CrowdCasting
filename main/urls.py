from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from main.views import ActorViewSet, ExperienceViewSet, ContactInfoViewSet

actor_list = ActorViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

actor_detail = ActorViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

contactinfo_detail = ContactInfoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

experience_detail = ExperienceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    url(r'^actors/$', actor_list, name='actor-list'),
    url(r'^actors/(?P<pk>[0-9]+)/$', actor_detail, name='actor-detail'),
    url(r'^experience/(?P<pk>[0-9]+)/$',
        experience_detail, name='experience_detail'),
    url(r'^contactinfo/(?P<pk>[0-9]+)/$',
        contactinfo_detail, name='contactinfo_detail'),
])


# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
