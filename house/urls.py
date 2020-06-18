from django.urls import path, include
from rest_framework import routers

from house import views as accounts


router = routers.DefaultRouter()
router.register(r'manager_house', accounts.HouseViewSet, 'manager_house')
router.register(r'staff_house', accounts.HouseStaffViewSet, 'staff_house')
router.register(r'build_num', accounts.BuildNumViewSet, 'build_num')


urlpatterns = [
    path('', include(router.urls)),
]
