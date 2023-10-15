from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from diasyncserver.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q
import csv
from io import TextIOWrapper
viewset = viewsets.ModelViewSet

class EmailAuthBackend(object):
    def authenticate(self, request, email=None, password=None):
        print("Hey there")
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email= request.email)
        except UserModel.DoesNotExist:
            return None

        if not user.check_password(request.password):
            return None
        else:
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
    permission_classes = [permissions.AllowAny]

@api_view(['POST'])
@permission_classes([])
def login_view(request):
  # Attempt to authenticate the user
  user = get_user(username=request.data.get('email'))

  if user:
    checkpass = user.check_password(request.data.get('password'))
    if checkpass:      
      # If authentication is successful, generate or retrieve a token
      token, created = Token.objects.get_or_create(user=user)
      return Response({
        'message': 'Login successful',
        'token': token.key,
        'user': {
          'id': user.id,
          'firstname': f"{user.first_name} {user.last_name}",
          'username': user.username,
          'email': user.email,
        }
      }, status=status.HTTP_200_OK)

    else:
      # If authentication fails, provide a clear error message
      return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
  
  else:
      # If authentication fails, provide a clear error message
    return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
  
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_view(request):
    try:
        user = Users.objects.get(email=request.data.get('email'))
    except Users.DoesNotExist:
        user = None

    if user is None:
        csv_file = request.FILES.get('data')

        if csv_file:
            text_data = TextIOWrapper(csv_file.file, encoding='utf-8')
            csv_reader = csv.reader(text_data, delimiter=',')
            next(csv_reader, None)

            user = Users(
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                email=request.data.get("email"),
                password=request.data.get("password"),
                weight=request.data.get("weight"),
                height=request.data.get("height"),
                sex=request.data.get("sex"),
                diabetes_type=request.data.get("type"),
            )

            for row in csv_reader:
                date_time, blood_sugar, _, _, carbs, _ = row
                GlucoseReading.objects.create(
                    user=user,
                    date=timezone.now(),  # Set the date as needed
                    time=datetime.datetime.strptime(date_time, "%d/%m/%Y %H:%M").time(),
                    blood_sugar_level=float(blood_sugar),
                )

            user.save()

            return Response({
                'message': "User Registered",
                'name': f"{user.first_name} {user.last_name}",
                'password': user.password,
                'Diabetes type': user.diabetes_type
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'CSV file missing, user not created.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'User already exists'}, status=status.HTTP_409_CONFLICT)





