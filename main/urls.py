from django.conf.urls import url, include
from main import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'head_shots', views.HeadShotsViewSet)
router.register(r'trial', views.TrialViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'actor', views.ActorViewSet, base_name='actor')
router.register(r'experience', views.ExperienceViewSet, base_name='experience')
router.register(r'request_account', views.RequestAccountViewSet)

experience_detail = views.ExperienceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^experience/(?P<pk>[0-9]+)/$',
        experience_detail, name='experience_detail'),
]
