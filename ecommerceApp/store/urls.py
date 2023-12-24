from django.urls import path
from . import views


urlpatterns = [
    path('',views.store,name="store"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    
    path('update_item/',views.updateItem,name="update_item"),
]

# authentication_form=LoginForm