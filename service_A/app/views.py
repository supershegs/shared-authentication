import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # import pdb
        # pdb.set_trace()
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        print(user)
        if user:
            # Generate JWT Token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            # import pdb
            # pdb.set_trace()
            print(refresh)
            print(access_token)
            print(user.id), 
            print(user.email)
            print(user.username)
            user_data = {
                "user_id": user.id,
                "username": user.username,
                # "email": user.email,
                # "role": user.role,  # Assuming 'role' field exists in the user model
            }

            # Store token in Redis (key: token, value: username)
            settings.REDIS_CLIENT.setex(access_token, 3600, json.dumps(user_data))  # 1 hour expiry

            # settings.REDIS_CLIENT.setex(access_token, 3600, user_data) 

            return Response({"access_token": access_token})
        return Response({"error": "Invalid credentials"}, status=401)
