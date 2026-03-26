from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'currency',
            'image_url', 'product_url', 'category', 'rating',
            'in_stock', 'source', 'scraped_at', 'created_at',
        ]


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list endpoints."""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'currency', 'image_url',
            'category_name', 'rating', 'in_stock', 'scraped_at',
        ]
