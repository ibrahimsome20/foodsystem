from rest_framework import serializers
from .models import *

class CatogerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catogery
        fields = '__all__'


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

        
class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Username
        fields = '__all__'
        extra_kwargs = {'password_user': {'write_only': True}}