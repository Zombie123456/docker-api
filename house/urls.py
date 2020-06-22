from django.urls import path, include
from rest_framework import routers

from house import views as house


router = routers.DefaultRouter()
router.register(r'house', house.HouseViewSet, 'manager_house')
router.register(r'build_num', house.BuildNumViewSet, 'build_num')
router.register(r'community', house.CommunityViewSet, 'community')
router.register(r'import_log', house.ImportLogViewSet, 'import_log')


urlpatterns = [
    path('', include(router.urls)),
    path('import_file/', house.import_excel_file),
    path('import_car_file/', house.import_car_excel_file),
]
