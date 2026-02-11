from rest_framework import generics, permissions
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated
from .models import Category, MenuItem, Cart, Order
from .serializers import (
    CategorySerializer,
    MenuItemSerializer,
    CartSerializer,
    OrderSerializer,
    MenuItemUpdateSerializer,
    OrderUpdateSerializer
)

# Custom Permissions

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists() or request.user.is_superuser


class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Delivery').exists() or request.user.is_superuser


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Customer').exists() or request.user.is_superuser


# Category API (only admin can create and view)

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


# MenuItem API
# GET → Public
# POST → Manager or Admin only

class MenuItemList(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsManager()]
        return [permissions.AllowAny()]



# Manager: Update "Item of the Day" (featured field)

class MenuItemUpdate(generics.UpdateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemUpdateSerializer
    permission_classes = [IsManager]


# Cart API (Authenticated users only)
# Users can view and add items to their cart

class CartList(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Order API (Authenticated users only)
# Users can view and create their own orders

class OrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)

        cart_items = Cart.objects.filter(user=self.request.user)
        total = 0

        for item in cart_items:
            order.order_items.create(
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )
            total += item.price

        order.total = total
        order.save()
        cart_items.delete()


# Manager: Assign delivery crew and update order status

class OrderAssign(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsManager]


# Delivery Crew: Mark assigned orders as delivered

class OrderDeliveryUpdate(generics.UpdateAPIView):
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsDeliveryCrew]

    def get_queryset(self):
        # Delivery crew can only see orders assigned to them
        return Order.objects.filter(delivery_crew=self.request.user)
