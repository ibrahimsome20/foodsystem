from django.urls import path
from .views import *

urlpatterns = [
    path('category/', category_list),
    path('food/', food_list),
    path('food/delete/<int:id>/', delete_food),

    path('cart/add/', add_to_cart),
    path('cart/<str:session_id>/', cart_items),
    path('admin-login/', admin_login_api),
     path('register/', register_user),
    path('login/', login_user),
    path('order/', create_order),
    path('users/', get_users),

]
