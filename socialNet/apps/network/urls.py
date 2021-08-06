from django.contrib.auth import logout
from socialNet.settings import LOGOUT_REDIRECT_URL
from django.urls import path
from . import views
from django.contrib.auth import views as authViews

urlpatterns = [
    path('', views.main, name='main'),
    path('account', views.account, name='account'),
    path('signup', views.register, name='signup'),
    path('signin', views.LogInView.as_view(), name='signin'),
    path('logout', authViews.LogoutView.as_view(), name='logout'),
]
