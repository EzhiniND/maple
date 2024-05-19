from django.urls import path
from django.views.generic import TemplateView
from . import views 


urlpatterns= [
    path('register/',views.register,name="register"),
    path('',views.user_login,name="login"),
    path('products/', views.product_list, name='product_list'),
    path('remove_from_cart/<str:product_name>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/<str:product_name>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('search/', views.search_products, name='search_products'),
    path('login/',views.user_login,name="login"),
    path('home/',views.home,name="home"),
    path('submit-order/', views.submit_order, name='submit_order'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('logout/', views.log_out, name="logout"),


]    