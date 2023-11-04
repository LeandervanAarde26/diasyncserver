from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from diasyncserver.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
import csv
from io import BytesIO
import base64
import pandas as pd
from django.core.cache import cache
from datetime import datetime, date, timedelta
import calendar
import openai
from django.http import JsonResponse
from decouple import config
import json
from .Chat.main import main
from django.core import serializers

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


def format_glucose_readings_as_text(glucose_readings):
    formatted_text = ""
    for reading in glucose_readings:
        formatted_text += f"Date: {reading.date} Time: {reading.time} Glucose_level: {reading.blood_sugar_level} \n" 

    return formatted_text


@api_view(['GET'])
def get_analysed_data(request):
    user_id = request.query_params.get('userid')
    cache_key = f'glucose_readings_{user_id}'
    readings = cache.get(cache_key)
    current_month_name = calendar.month_name[date.today().month]
    today = date.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    previous_month_name = calendar.month_name[last_day_of_previous_month.month]

    if readings is None:
        readings = GlucoseReading.objects.all().prefetch_related('user')

    if user_id is not None:
        readings = readings.filter(user__id=user_id)

    cache.set(cache_key, readings, timeout=60)

    glucose_data = format_glucose_readings_as_text(readings)
    openai.api_key = config('OPEN_AI_KEY')
    user_message = f"""
Please generate a JSON response in the following format:
{{
"analysisData" : {{
"{current_month_name}" : {{
    "stable": ,
    "low": ,
    "high":,
    "unstable:
}},
"{previous_month_name}" : {{
    "stable": ,
    "low": ,
    "high":,
    "unstable:
}}
}},

"Observation": "",
  "DietarySuggestions": [
    {{
      "heading": "",
      "description": "",
      "link": ""
    }},
    {{
      "heading": "",
      "description": "",
      "link": ""
    }}
  ],

  "AnalysisSuggestions": [
    {{
      "heading": "",
      "description":"",
      "link": ""
    }},
    {{
      "heading": "",
      "description": "",
      "link": ""
    }}
  ]
}}
The response should include the following information:

* Two Dietary changes to consider based based on my glucose readings in `blood_sugar_level` {glucose_data}. For example, if my bloodusgar patterns show more high bloodugar, there should be a dietary change that includes less carbohydrate intake. Or if my patterns show low bloodusgar at night, there should be an adjustment that can push my glucose up slightly so that it doesn't drop at a certain time.  Each dietary recommendation should include a heading, description, and one relevant link to a recipe
* Two concise articles on how to better manage my Diabetes based on my glucose readings in `blood_sugar_level` {glucose_data}. Each recommendation should include a heading, description, and one relevant link.
* One Observation that you've made about my bloodsugar based on my trends that you can identify in `blood_sugar_level` {glucose_data}, this observation should be in the 'Observation' section
* Split the data into two parts, one half should be for the previous month and the other half contains the data for this month, each months data should be analysed and have the following outCome: 
in the `[monthName]` field, indicate:
    "stable": using a number the % of stable bloodusgar for that month ,
    "low": using a number the % of low bloodusgar for that month ,
    "high":  using a number the % of high bloodusgar for that month,
    "unstable: using a number the % of unstable bloodusgar for that month,

In the case that there is no previous month data, indicate that in the [monthName] field such as 
[monthName]: null,

Please note that the response must be in the exact JSON format specified above.
Here is an example of the desired JSON response:
NOTE: Always use double quotations, never single quotations
{{
"analysisData": {{
  "{previous_month_name}": null,
  "{current_month_name}":  {{
    "stable": 20,
    "low": 15,
    "high": 65
  }}
}}

  "DietarySuggestions": [
    {{
          "heading": "Chicken Breasts",
      "description": "Chicken breasts are a great food to eat when you have high bloodsugar due to its lack of carbohydrates and high protein...",
      "link": "https://WhatsforDinnerExampleLink.com"
    }},
    {{
          "heading": "Eggs  ",
      "description": "Eggs breasts are a great food to eat when you have high bloodsugar due to its lack of carbohydrates and high protein...",
      "link": "https://WhatsforDinnerExampleLink.com"
    }}
  ],
  "AnalysisSuggestions": [
    {
        {
      "heading": "Understanding High bloodusgar",
      "description": "High blood sugar (hyperglycaemia) is where the level of sugar in your blood is too high. It mainly affects people with diabetes and can be serious if not treated.",
      "link": "https://www.nhs.uk/conditions/high-blood-sugar-hyperglycaemia/#:~:text=High%20blood%20sugar%20(hyperglycaemia)%20is,low%20blood%20sugar%20(hypoglycaemia)."
        }
    },
    {
      {
      "heading": "8 Ways to lower bloodsugar",
      "description": "High blood sugar, also known as hyperglycemia, is associated with diabetes, a disease that can cause heart attack, heart failure, stroke, and kidney failure. High blood sugar occurs when your body fails to produce enough insulin or use insulin efficiently. The Centers for Disease Control and Prevention estimates 13% of all Americans and 25% of those 65 or older suffer from it. ",
      "link": "https://www.gradyhealth.org/blog/8-ways-to-lower-your-blood-sugar/"
      }
    }
  ]
}}
}}
"""

    chat_completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )

    generated_text = chat_completion.choices[0].message['content']

    return JsonResponse({'Response': generated_text}, status = status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def post_new_readings(request):
    user_id = request.query_params.get('userid')
    cache_key = f'glucose_readings_{user_id}'
    readings = cache.get(cache_key)


    if readings is None:
        readings = GlucoseReading.objects.all().prefetch_related('user')

        if user_id is not None:
            readings = readings.filter(user__id=user_id)
            user = Users.objects.get(id = user_id)
            print(user)
        cache.set(cache_key, readings, timeout=60)

    serializer = GlucoseSerializer(readings, many=True)

    csv_file = request.data.get('data')

    print(csv_file)
    decoded_data = base64.b64decode(csv_file.split(',', 1)[1])
    csv_stream = BytesIO(decoded_data)

    incoming_data = pd.read_csv(csv_stream, dtype=str)
    incoming_data_df = pd.DataFrame(incoming_data, columns=['Time', 'Blood Sugar [mmol/L]'])
    incoming_data_df = incoming_data_df.sort_values(by='Time', ascending=False)

    existing_df = pd.DataFrame(serializer.data, columns=['time', 'date', 'blood_sugar_level', 'user'])
    existing_df['Time'] = existing_df["date"]  +" "+ existing_df["time"]
    existing_df.drop(['date', 'time'], axis=1, inplace=True)
    existing_df['Time'] = pd.to_datetime(existing_df['Time'])
    existing_df['Time'] = existing_df['Time'].dt.strftime('%d/%m/%Y %H:%M')
    existing_df = existing_df.sort_values(by='Time', ascending=False)

    # last_entry = existing_df.iloc[0]
    # last_entry_index = initial_data_df[initial_data_df['Time'] == last_entry['Time']].index[0]
    # initial_data_df = initial_data_df.iloc[:last_entry_index -2]
    incoming_data_df.drop(incoming_data_df[incoming_data_df['Time'] < existing_df.iloc[0]['Time']].index, inplace=True)

    for _, row in incoming_data_df.iterrows():
       GlucoseReading.objects.create(
          user=user,
          date=  datetime.strptime(row['Time'], "%d/%m/%Y %H:%M").date(),
          time= datetime.strptime(
          row['Time'], "%d/%m/%Y %H:%M").time(),
          blood_sugar_level=float(row['Blood Sugar [mmol/L]']),
      )
    
    return Response({'message': incoming_data_df}, status=status.HTTP_201_CREATED)

    

@api_view(['GET'])
def get_complications(request):
    user_id = request.query_params.get('userid')
    cache_key = f'glucose_readings_{user_id}'
    readings = cache.get(cache_key)

    if readings is None:
        readings = GlucoseReading.objects.all().prefetch_related('user')

    if user_id is not None:
        readings = readings.filter(user__id=user_id)

    cache.set(cache_key, readings, timeout=60)

    glucose_data = format_glucose_readings_as_text(readings)
    openai.api_key = config('OPEN_AI_KEY')
    user_message = f"""
Please generate a JSON response in the following format:
{{
  "complications": [
    {{
      "heading": "",
      "description": ",
      "link": ""
    }},
    {{
      "heading": "",
      "description": ",
      "link": ""
    }},
    {{
      "heading": "",
      "description": ",
      "link": ""
    }},
  ],
  "blood_sugar_status": "",
  "blood_sugar_distribution": {{
    "stable": ,
    "low": ,
    "high":
  }}

The response should include the following information:

* Three concise long-term health complications based on my glucose readings in `blood_sugar_level` {glucose_data}. Each complication should include a heading, description, and relevant links.
* An indicator of whether my blood sugar is high, low, or stable with a `consideration` field.
* The percentages of stable, low, and high blood sugar in an array.

Please note that the response must be in the exact JSON format specified above.

Here is an example of the desired JSON response:

{{
  "complications": [
    {{
      "heading": "Diabetic Retinopathy",
      "description": "Diabetic retinopathy is damage to the blood vessels in the retina, the light-sensitive tissue at the back of the eye. It is a common complication of diabetes and can lead to blindness.",
      "link": "https://www.mayoclinic.org/diseases-conditions/diabetic-retinopathy/symptoms-causes/syc-20371626"
    }},
    {{
      "heading": "Diabetic Neuropathy",
      "description": "Diabetic neuropathy is nerve damage caused by diabetes. It can affect any nerve in the body, but most commonly affects the nerves in the feet and legs.",
      "link": "https://www.mayoclinic.org/diseases-conditions/diabetic-neuropathy/symptoms-causes/syc-20371580"
    }},
    {{
      "heading": "Diabetic Kidney Disease",
      "description": "Diabetic kidney disease is damage to the kidneys caused by diabetes. It is a leading cause of kidney failure in the United States.",
      "link": "https://www.mayoclinic.org/diseases-conditions/diabetic-kidney-disease/symptoms-causes/syc-20371628"
    }}
  ],
  "blood_sugar_status": "High",
  "blood_sugar_distribution": {{
    "stable": 20,
    "low": 15,
    "high": 65
  }}
}}
"""

    chat_completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )

    generated_text = chat_completion.choices[0].message['content']

    return JsonResponse({'Response': generated_text}, status = status.HTTP_200_OK)



@api_view(["POST"])
@permission_classes([])
def conversation(request):
  user_id = request.query_params.get('userid')
  cache_key = f'glucose_readings_{user_id}'
  readings = cache.get(cache_key)
  message = request.data.get("message")

  if readings is None:
    readings = GlucoseReading.objects.all().prefetch_related('user')

  if user_id is not None:
    readings = readings.filter(user__id=user_id)
    cache.set(cache_key, readings, timeout=60)
  
  glucose_data = format_glucose_readings_as_text(readings)

  conversation = main(message, glucose_data)

  print(conversation)
  # response = serializers.serialize("json", conversation)
  content = conversation[-1].content
  content = json.dumps(content)
  print(content)

  return JsonResponse(content,safe = False, status = status.HTTP_200_OK)


  
  
