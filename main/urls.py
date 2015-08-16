from django.conf.urls import url, include
from main.views import (
    ActorViewSet, ExperienceViewSet, ContactInfoViewSet,
    RequestContactInfoViewSet,
    TagViewSet, EducationViewSet)
from main import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.

actor_list = ActorViewSet.as_view({
    'get': 'list',
    'post': 'create',
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

request_contactinfo = RequestContactInfoViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

tag_detail = TagViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

education_detail = EducationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

router = DefaultRouter()
router.register(r'head_shots', views.HeadShotsViewSet)
router.register(r'trial', views.TrialViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'actor', views.ActorViewSet, base_name='actor')
router.register(r'experience', views.ExperienceViewSet, base_name='experience')
router.register(r'request_account', views.RequestAccountViewSet)
router.register(r'contactinfo', ContactInfoViewSet, base_name='contactinfo')
router.register(r'request_contactinfo', RequestContactInfoViewSet)
router.register(r'profile_pictures', views.ProfilePictureViewSet)
router.register(r'tags', TagViewSet, base_name='tag')
router.register(r'education', EducationViewSet, base_name='education')


urlpatterns = [
    url(r'^', include(router.urls)),
    ]
