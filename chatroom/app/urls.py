from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'registration', views.registration_page, name="registration_page"),
    url(r'register', views.register, name="registration"),
    url(r'login_user', views.login_user, name="login_user"),
    url(r'^login', views.login, name="login"),
    url(r'^home', views.home, name="home"),
    url(r'list_users', views.list_users, name="list_users"),
]
