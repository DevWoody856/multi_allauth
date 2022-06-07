from allauth.account.views import LogoutView
from django.urls import path
from . import views

app_name = 'two_app'


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('accounts/login/', views.ShopLogin.as_view(), name='shop-signup'),
    path('accounts/login-customer/<slug:shop_name>/<uuid:shopId>/', views.customer_login, name='customer-login'),
    path('accounts/shop/shop-name-create/<uuid:shopId>/', views.shopNameCreate, name='shop-name-create'),
    path('accounts/shop/<uuid:shopId>/', views.shopProfile, name='shop-profile'),
    path('accounts/customer/<slug:shop_name>/<uuid:shopId>/', views.customer_profile, name='customer-profile'),
    path('accounts/account_logout/', LogoutView.as_view(), name='account_logout'),
]