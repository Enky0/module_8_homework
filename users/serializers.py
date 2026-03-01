from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'phone', 'avatar', 'city', 'is_active', 'last_login')

        avatar = serializers.ImageField(required=False, allow_null=True)
