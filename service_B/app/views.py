from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from b_config.authentication import RedisTokenAuthentication

class ProtectedView(APIView):
    authentication_classes = [RedisTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": f"Hello, {request.user}! : user id: {request.user.id} and username: {request.user.username}"
        })
