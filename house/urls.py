from django.urls import path, include
from rest_framework import routers

from house import views as house


router = routers.DefaultRouter()
router.register(r'manager_car', house.CarViewSet, 'manager_house')
router.register(r'manager_house', house.HouseViewSet, 'manager_house')
router.register(r'seller_house', house.HouseStaffViewSet, 'seller_house')
router.register(r'seller_car', house.HouseStaffViewSet, 'seller_house')
router.register(r'build_num', house.BuildNumViewSet, 'build_num')


urlpatterns = [
    path('', include(router.urls)),
    path('import_file/', house.import_excel_file),
    path('import_car_file/', house.import_car_excel_file),
]
