from SiteApp import views
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from SiteApp import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('Register/', views.User_Register_page),
    path('Login/', views.User_Login_page),
    path('User_Logout/', views.User_logout),
    path('User_Register_Data/', views.User_Register_Data),
    path('User_login/', views.User_Login),
    path('shop_page/', views.shop_page),
    path('product_details/', views.product_details_page),
    path('cart_page/', views.cart_page),
    path('adding_cart_items/', views.adding_cart_items),
    path('product_details/<int:id>/', views.product_details_page),
    path('checkout_page/', views.checkout_page),
    path('order_items/', views.order_items),
    path('order_invoice/', views.order_invoice),
    path('orders/', views.my_orders),
    path('profile/', views.user_profile),
    path('remove_cart_items/<int:id>/', views.remove_cart_items),
    path('update_user/<int:id>/', views.update_user_data),
    path('change_password/<int:id>/', views.User_password_change),
    

]