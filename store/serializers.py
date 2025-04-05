from rest_framework import serializers
from uuid import uuid4
from .models import Genre, Book, Author, Customer, Order, Review, Cart, CartItem

class GenraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'title', 'product_count']

    product_count = serializers.IntegerField(read_only=True)

class AuthorSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    short_bio = serializers.SerializerMethodField()
    total_books = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'title', 'bio', 'short_bio', 'total_books', 'image', 'created_at', 'updated_at']

    def get_short_bio(self, obj):
        return obj.bio[:100] + "..." if len(obj.bio) > 100 else obj.bio
    
    def get_total_books(self, obj):
        return obj.books.count()

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='Genre.title', read_only=True)
    genre_name = serializers.CharField(source='Genre.title', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    total_reviews = serializers.IntegerField(read_only=True)
    #cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'stock', 'isbn', 'price',
            'author', 'author_name', 'genre', 'genre_name', 'cover_image',
            'average_rating', 'total_reviews', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'description', 'score', 'image','created_at']
        read_only_fields = ['user', 'book', 'created_at']

    def create(self, validated_data):
        book_id = self.context['book_id']
        user = self.context['request'].user  # Get the authenticated user
        review, created = Review.objects.update_or_create(
            book_id=book_id, user=user,
            defaults={
                'score': validated_data['score'],
                'description': validated_data['description'],
                'image': validated_data['image'],
            }
        )
        
        return review
    
class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        validated_data['order_number'] = f'ORD-{uuid4().hex[:10].upper()}'
        return super().create(validated_data)
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    book = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.book.price

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.book.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField()

    def validate_book_id(self, value):
        if not Book.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No book with the given ID was found.'
            )
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        book_id = self.validated_data['book_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, book_id=book_id
            )
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


    

    

    
