from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'in_stock', 'source', 'scraped_at']
    list_filter = ['category', 'in_stock', 'source']
    search_fields = ['title', 'description']
    readonly_fields = ['scraped_at', 'created_at']
