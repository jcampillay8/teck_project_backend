# backend/apps/user/serializers.py

# Installed Utils
from rest_framework import serializers

# App Utils
from apps.authentication.models import CustomUser

# Serializer for user data reading and updating
class UserInfoSerializer(serializers.ModelSerializer):
    """
    Is used to specify which user fields should be read and updated
    """
    is_superuser = serializers.BooleanField(read_only=True)  # Añadir campo para is_superuser

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'is_superuser']  # Incluir is_superuser
        read_only_fields = ['id', 'email', 'is_superuser']  # Evitar que el ID y el email sean editables
