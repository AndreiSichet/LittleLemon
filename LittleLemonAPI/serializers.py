from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User

# Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

# MenuItem
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'category', 'featured']

# Serializer to update item of the day (featured)
class MenuItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'featured']

# Cart
class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)  

    
    menuitem_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='menuitem', write_only=True
    )

    class Meta:
        model = Cart
        fields = ['id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']

# OrderItem
class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']

# Order
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    delivery_crew = serializers.StringRelatedField() 
    user = serializers.StringRelatedField(read_only=True)  

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items']
# Serializer for manager/delivery update (atribution of delivery crew and status)
class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['delivery_crew', 'status']
