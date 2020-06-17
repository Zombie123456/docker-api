from django.conf.urls import url
from loginsvc import views as loginsvc


urlpatterns = [
    url(r'^login/$', loginsvc.login, name='member_login'),
    url(r'^manage/login/$', loginsvc.login, name='manage_login'),
    url(r'^my/$', loginsvc.current_user, name='current_user'),
    url(r'^logout/$', loginsvc.logout, name='logout'),
    url(r'^reset_password/$', loginsvc.reset_password, name='reset')
]
