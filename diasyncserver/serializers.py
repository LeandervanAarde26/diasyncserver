from rest_framework import serializers
from api.models import *
from django.contrib.auth.hashers import make_password

serializer = serializers.ModelSerializer

from rest_framework import serializers
from api.models import Users, Group

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())

    class Meta:
        model = Users
        # fields = "__all__"
        exclude = ['password']

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])

        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        username = f"{first_name.lower()}{last_name.lower()}".strip()  
        validated_data['username'] = username 
        validated_data['password'] = make_password(validated_data['password'])
      
        user = Users.objects.create(**validated_data)


        user.groups.set(groups_data)

        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove unwanted fields
        fields_to_remove = ['is_staff', 'is_active', 'date_joined']
        for field in fields_to_remove:
            data.pop(field, None)
        # Set default values
        data['is_superuser'] = False
        data['is_active'] = True
        return data
    
    
class GlucoseSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = GlucoseReading
        fields = '__all__'

    def get_user(self, obj):
        if obj.user:
            user_serializer = UserSerializer(obj.user)
            return user_serializer.data
        else:
            return None

    
