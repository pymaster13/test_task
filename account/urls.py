from django.urls import path, re_path

from .views import index, register, activate, user_login, user_logout

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login , name='login'),
    path('logout/', user_logout , name='logout'),
    path('register/', register , name='register'),
    
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
]
