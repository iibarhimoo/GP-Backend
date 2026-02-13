from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .authentication import verify_firebase_token

User = get_user_model()

class UserSyncView(APIView):
    """
    POST /api/v1/users/sync
    This endpoint bridges Firebase and MySQL.
    """
    permission_classes = [AllowAny]
    authentication_classes = []  

    def post(self, request):
        try:
            
            decoded_token = verify_firebase_token(request)
            if not decoded_token:
                return Response({"error": "Invalid token payload"}, status=401)
        except Exception as e:
            return Response({"error": str(e)}, status=401)
            
        uid = decoded_token.get('uid')
        email = decoded_token.get('email', '')

        # Syncing Firebase UID with local MySQL record
        user, created = User.objects.get_or_create(
            username=uid, 
            defaults={'email': email, 'is_active': True}
        )

        return Response({
            "status": "success",
            "local_id": user.id,
            "created": created
        }, status=status.HTTP_200_OK)