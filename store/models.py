from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf import settings
from django.core.validators import MinValueValidator
from uuid import uuid4
from django.utils.text import slugify
from django.utils import timezone  
from .validation import validate_cover_image_size, validate_image_file_size, validate_author_image_size

# Genre Model
class Genre(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, blank=True)
    featured_book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# Author Model
class Author(models.Model):
    title = models.CharField(max_length=255)
    bio = models.TextField()
    image = models.ImageField(upload_to='authors/', validators=[validate_author_image_size, validate_image_file_size], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Book Model
class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    stock = models.IntegerField()
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,related_name='books')
    cover_image = models.ImageField(upload_to='book_covers/', validators=[validate_cover_image_size, validate_image_file_size], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def average_rating(self):
        ratings = self.ratings.all()
        return round(sum(r.score for r in ratings) / ratings.count(), 1) if ratings.exists() else 0

    def total_reviews(self):
        return self.ratings.count()

    def __str__(self):
        return self.title

# Review Model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="ratings", on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    description = models.TextField()
    image = models.ImageField(upload_to='review_img/', validators=[validate_image_file_size], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"Review for {self.book.title} by {self.user.username}"

# Customer Model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [('view_history', 'Can view history')]

# Address Model
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

# Order Model
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=20, unique=True, blank=True, null=True, editable=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f'ORD-{uuid4().hex[:10].upper()}'
        super().save(*args, **kwargs)

    class Meta:
        permissions = [('cancel_order', 'Can cancel order')]

# OrderItem Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

# Cart Model
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'book']]
