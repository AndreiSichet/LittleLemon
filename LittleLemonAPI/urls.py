from django.urls import path
from . import views
from .views import CategoryList, MenuItemList, CartList, OrderList

urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('menu-items/', views.MenuItemList.as_view(), name='menuitem-list'),
    path('cart/', CartList.as_view(), name='cart-list'),
    path('orders/', OrderList.as_view(), name='order-list'),
    path('menu-items/<int:pk>/update/', views.MenuItemUpdate.as_view(), name='menuitem-update'),
    path('orders/<int:pk>/assign/', views.OrderAssign.as_view(), name='order-assign'),
    path('orders/<int:pk>/deliver/', views.OrderDeliveryUpdate.as_view(), name='order-deliver'),

]
