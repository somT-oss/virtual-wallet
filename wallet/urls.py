from unicodedata import name
from django.urls import path
from . import views 


urlpatterns = [
    path("all-wallets", views.all_wallets, name="all-wallets"),
    path("get-wallet/<int:id>", views.user_wallet_view, name="view-user-wallet"),
    path("fund-user-wallet/<int:id>", views.fund_single_wallet, name='fund-single-wallet'),
    path("fund-all-wallet", views.fund_all_wallet, name='fund-all-wallet'),
    path("delete", views.delete_all_wallets, name="delete-all-wallets")
]