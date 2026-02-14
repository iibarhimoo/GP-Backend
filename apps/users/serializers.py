from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import MedicalProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'date_joined']
