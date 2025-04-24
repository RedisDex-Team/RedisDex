"""redisdex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from store.views import home, registro, shop, cart, test_session_view, add_to_cart, increase_qty, decrease_qty, place_order, profile_view, edit_profile, card_detail, clear_search_history, order_confirmation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', registro, name='register'), 
    path('shop/', shop, name='shop'),
    path('cart/', cart, name='cart'),
    path("test-sesion/", test_session_view, name="test_sesion"),
    path('cart/add/<int:card_id>/', add_to_cart, name='add_to_cart'),
    path('cart/increase/<str:card_id>/', increase_qty, name='increase_qty'),
    path('cart/decrease/<str:card_id>/', decrease_qty, name='decrease_qty'),
    path('place-order/', place_order, name='place_order'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('card/<int:card_id>/', card_detail, name='card_detail'),
    path('profile/clear-search-history/', clear_search_history, name='clear_search_history'),
    path('order/<int:order_id>/confirmation/', order_confirmation, name='order_confirmation'),
    path('place-order/', place_order, name='place_order'),
]
