from rest_framework import serializers
from api.models import *

serializer = serializers.ModelSerializer

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())

    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email', 'password', 'weight', 'height', 'diabetes_type', 'sex', 'groups')

    def create(self, validated_data):
        # Extract the groups data and remove it from the validated data
        groups_data = validated_data.pop('groups', [])

        # Create the user instance without the groups
        user = Users.objects.create(**validated_data)

        # Add the user to the groups
        user.groups.set(groups_data)

        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove unwanted fields
        fields_to_remove = ['username', 'is_staff', 'is_active', 'date_joined']
        for field in fields_to_remove:
            data.pop(field, None)
        # Set default values
        data['is_superuser'] = False
        return data

    
