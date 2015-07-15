from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from main.views import ActorViewSet, ExperienceViewSet, ContactInfoViewSet
from main import views
from rest_framework.routers import DefaultRouter

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

router = DefaultRouter()
router.register(r'head_shots', views.HeadShotsViewSet)
router.register(r'trial', views.TrialViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'actor', views.ActorViewSet)
router.register(r'experience', views.ExperienceViewSet)
router.register(r'contactinfo', ContactInfoViewSet, base_name='contactinfo')

urlpatterns = [
    url(r'^', include(router.urls)),
    ]
