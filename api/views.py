from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from diasyncserver.serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q
viewset = viewsets.ModelViewSet

class EmailAuthBackend(object):
    def authenticate(self, request, email=None, password=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None

        if not user.check_password(password):
            return None

        return user

def get_user(username):
    UserModel = get_user_model()
    try:
        return UserModel.objects.get(email=username)
    except UserModel.DoesNotExist:
        return None
    
class UserViewSet( viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([])
def login_view(request):
    # Attempt to authenticate the user
    user = get_user(username=request.data.get('email'))

    if user:
        # If authentication is successful, generate or retrieve a token
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user': {
                'id': user.id,
                'firstname': f"{user.first_name} {user.last_name}",
                'email': user.email,
            }
        }, status=status.HTTP_200_OK)

    else:
        # If authentication fails, provide a clear error message
        return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
