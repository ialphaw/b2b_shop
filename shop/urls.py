from django.urls import path, include
from rest_framework import routers

from shop import views

router = routers.DefaultRouter()
router.register(r"user_credit", views.UserCreditViewSet, basename="user_credit")
router.register(r"charge", views.ChargeViewSet, basename="charge")

url_urlpatterns = [
    path("", include(router.urls)),
]
