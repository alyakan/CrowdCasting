from django.conf.urls import url, include
from main import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'head_shots', views.HeadShotsViewSet)
router.register(r'trial', views.TrialViewSet)
router.register(r'user', views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
