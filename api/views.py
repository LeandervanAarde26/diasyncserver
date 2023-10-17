from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
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
from django.core.cache import cache
from datetime import datetime


viewset = viewsets.ModelViewSet


class EmailAuthBackend(object):
    def authenticate(self, request, email=None, password=None):
        print("Hey there")
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=request.email)
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


class UserViewSet(viewsets.ModelViewSet):
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
        user.save()
        default_group = Group.objects.get(name='Default')
        default_group.user_set.add(user)

        csv_file = request.data.get('data')
        decoded_data = base64.b64decode(csv_file.split(',', 1)[1])
        csv_stream = BytesIO(decoded_data)
        initial_data = pd.read_csv(csv_stream, dtype=str)

        data = pd.DataFrame(initial_data, columns=[
                            'Time', 'Blood Sugar [mmol/L]'])

        for _, row in data.iterrows():
            GlucoseReading.objects.create(
                user=user,
                date=  datetime.strptime(row['Time'], "%d/%m/%Y %H:%M").date(),
                time= datetime.strptime(
                    row['Time'], "%d/%m/%Y %H:%M").time(),
                blood_sugar_level=float(row['Blood Sugar [mmol/L]']),
            )

        return Response({'message': 'User Registered'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'User already exists'}, status=status.HTTP_409_CONFLICT)


@api_view(['GET'])
def glucose_view(request):
  user_id = request.query_params.get('userid')
  start_date = request.query_params.get('start_date')
  end_date = request.query_params.get('end_date')

  cache_key = f'glucose_readings_{user_id}_{start_date}_{end_date}'
  readings = cache.get(cache_key)

  if readings is None:
    readings = GlucoseReading.objects.all().prefetch_related('user')

    if user_id is not None:
      readings = readings.filter(user__id=user_id)

    if start_date is not None and end_date is not None:
      readings = readings.filter(created_at__range=(start_date, end_date))

    cache.set(cache_key, readings, timeout=60)

  serializer = GlucoseSerializer(readings, many=True)

  return Response(serializer.data)

