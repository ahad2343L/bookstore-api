from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.mixins import *
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from .models import Genre, Author, Book, Customer, Order,  Review, Cart, CartItem
from .serializers import GenraSerializer, AuthorSerializer, BookSerializer, ReviewSerializer, CustomerSerializer, CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CartItemSerializer

# Create your views here.
class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenraSerializer
    permission_classes =[permissions.IsAdminUser]

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes =[permissions.IsAdminUser]

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReviewViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        book_id=self.kwargs.get('book_pk')
        if book_id is None:
            return Review.objects.none()
        return Review.objects.filter(book_id=book_id)

    def get_serializer_context(self):
        book_id = self.kwargs.get('book_pk')
        if book_id is None and getattr(self, 'swagger_fake_view', False):
            return {}  # Return an empty context for schema generation
        return {'book_id': book_id, 'request': self.request}
    
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.user.is_staff:  # Exclude admin users
            return Response({"error": "Admins are not customers."}, status=status.HTTP_403_FORBIDDEN)

        customer = Customer.objects.filter(user_id=request.user.id).first()
        if not customer:
            return Response({"error": "Customer does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__book').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('book')
