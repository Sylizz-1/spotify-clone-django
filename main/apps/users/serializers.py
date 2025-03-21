from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'password','full_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            phone=validated_data.get('phone', '')
        )
        return user