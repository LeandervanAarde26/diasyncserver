from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from diasyncserver.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
import csv
from io import StringIO, BytesIO
import base64
import pandas as pd


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

def parse_csv(file_path):
    with open(file_path, "r") as f:
        reader = csv.reader(f)

        for row in reader:
            pass

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
    print("Reach")
    print(request.data)
    try:
        user = Users.objects.get(email=request.data.get('email'))
    except Users.DoesNotExist:
        user = None
 
    if user is None:
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
            user.save()  # You need to save the user object to generate an ID.
            default_group = Group.objects.get(name='Default')  # Replace with the actual group name
            default_group.user_set.add(user)

            csv_file = request.data.get('data')
            decoded_data = base64.b64decode(csv_file.split(',', 1)[1])
            csv_stream = BytesIO(decoded_data)
            initialData = pd.read_csv(csv_stream, dtype=str)

            data = pd.DataFrame(initialData, columns=['Time', 'Blood Sugar [mmol/L]'])

            for _, row in data.iterrows():
                GlucoseReading.objects.create(
                    user=user,  # Assign the user object, not the user.id
                    date=timezone.now(),  # Set the date as needed
                    time=datetime.datetime.strptime(row['Time'], "%d/%m/%Y %H:%M").time(),
                    blood_sugar_level=float(row['Blood Sugar [mmol/L]']),
                )

            return Response({'message': 'User Registered'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'User already exists'}, status=status.HTTP_409_CONFLICT)





