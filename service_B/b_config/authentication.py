import jwt
import json
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomAuthenticatedUser:
    def __init__(self, user_data, is_authenticated=True):
        self.id = user_data.get("user_id")  
        self.username = user_data.get("username")
        self.is_authenticated = is_authenticated

    def __str__(self): 
        return self.username
    
    def __repr__(self):
        return f"<CustomAuthenticatedUser username={self.username}>"

class RedisTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header.split(" ")[1]
        user_json = settings.REDIS_CLIENT.get(token)
        
        if not user_json:
            raise AuthenticationFailed("Invalid or expired token")

        user = self.__extract_user(user_json)  

        try:
            decoded_token = jwt.decode(token, settings.SIGNING_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        user_data = {
            "user_id": user.get("id"),
            "username": user.get("username"),
            # "email": user.get("email"),
            # "role": user.get("role")
        }

        user = CustomAuthenticatedUser(user_data=user_data)
        return (user, token)  
   
    def __extract_user(self, user):
        if isinstance(user, bytes):  
            user = user.decode("utf-8")
        if isinstance(user, str):
            user = json.loads(user)
        return user

