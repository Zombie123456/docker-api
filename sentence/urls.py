from django.conf.urls import url, include

from rest_framework import routers
from sentence import views as sentence


member_router = routers.DefaultRouter()
member_router.register(r'^sentence',
                       sentence.SentenceMemberViewSet,
                       base_name='member_sentence')


manager_router = routers.DefaultRouter()
manager_router.register(r'^sentence',
                        sentence.SentenceManageViewSet,
                        base_name='manage_sentence')


urlpatterns = [
    url(r'^member/', include(member_router.urls)),
    url(r'manage/', include(manager_router.urls))
]
