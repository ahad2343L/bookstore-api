from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from store.models import Customer
from django.db import transaction
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create user
        user = serializer.save()
        
        # Create customer profile
        Customer.objects.create(
            user=user,
            phone=serializer.validated_data.get('phone', ''),
            birth_date=serializer.validated_data.get('birth_date', None)
        )
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }, status=status.HTTP_201_CREATED)
