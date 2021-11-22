"""test_project URL Configuration"""

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', include('testing.urls')),
    path('', include('account.urls')),
]
