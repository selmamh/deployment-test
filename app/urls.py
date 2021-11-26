from django.urls import path, include
from . import views
from .views import SearchResultsView
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='app-home'),
    path('searchresults/', SearchResultsView.as_view(), name='searchresults' ),
    path('search/', views.Search.as_view(), name='search'),
    path('register/', views.register_request, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'),  name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/app/'), name='logout'),
    path('addcart/',views.add_cart,name='addcart'),
    path('removecart/',views.remove_cart,name='removecart'),
    path('cart/',views.cart,name='cart'),
    
]
