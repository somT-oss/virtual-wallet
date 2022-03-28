from unicodedata import name
from django.urls import path 
from . import views 

urlpatterns = [
    path('register', views.register_employee, name='register'),
    path('login', views.login_employee, name='login'),
    path('get-user/<str:firstname>', views.get_user, name='get-user'),
    path('update-user/<str:firstname>', views.update_user, name='update-user'),
    path('admin', views.get_admin_info, name='admin')
]