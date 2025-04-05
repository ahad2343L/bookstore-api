from django.contrib import admin
from .models import Genre, Author, Book, Review, Customer, Address, Order, OrderItem, Cart, CartItem

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'price', 'stock', 'created_at')
    list_filter = ('genre', 'author', 'price')
    search_fields = ('title', 'isbn')
    autocomplete_fields = ('author', 'genre')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('book__title', 'user__username')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'birth_date')
    search_fields = ('user__first_name', 'user__last_name', 'phone')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'customer')
    search_fields = ('street', 'city', 'customer__user__first_name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'payment_status', 'total_amount', 'placed_at')
    list_filter = ('payment_status', 'placed_at')
    search_fields = ('order_number', 'customer__user__first_name')
    autocomplete_fields = ('customer', 'shipping_address')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'unit_price')
    search_fields = ('order__order_number', 'book__title')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0  # No extra empty rows
    readonly_fields = ['book', 'quantity']
    can_delete = True

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    search_fields = ['id']
    readonly_fields = ['id', 'created_at']
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'book', 'quantity']
    search_fields = ['cart__id', 'book__title']
    list_filter = ['book']
