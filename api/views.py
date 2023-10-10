from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from diasyncserver.serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate

viewset = viewsets.ModelViewSet

class UserViewSet( viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([])
def login_view(request):
    # Attempt to authenticate the user
    user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))

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
