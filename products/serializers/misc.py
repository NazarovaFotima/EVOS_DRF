from .order import *
from products.models.product import *
from rest_framework import serializers
from products.models.misc import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = "__all__"



class ProductSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'avg_rating', 'category', 'cost', 'price',  'created_at', 'stock']



class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductViewHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductViewHistory
        fields = '__all__'
