from unicodedata import name
from django.urls import path 
from . import views 

urlpatterns = [
    path('register', views.register_employee, name='register'),
    path('register/admin', views.create_admin_user, name='register-admin'),
    path('login', views.login_employee, name='login'),
    path('get-user/<str:firstname>', views.get_user, name='get-user'),
    path('update-user/<str:firstname>', views.update_user, name='update-user'),
    path("delete", views.delete_all_users, name="delete-users")
]