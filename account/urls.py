from django.urls import path, include
from rest_framework import routers

from account import views as accounts


router = routers.DefaultRouter()
router.register(r'staff', accounts.StaffViewSet, 'staff')
router.register(r'role', accounts.RoleViewSet, 'role')


urlpatterns = [
    path('', include(router.urls)),
]
