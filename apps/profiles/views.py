from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MedicalProfile
from .serializers import MedicalProfileSerializer

class MyProfileManageView(APIView):
    """
    GET /api/v1/profiles/me/  -> Fetch my profile
    POST /api/v1/profiles/me/ -> Create my profile
    PUT /api/v1/profiles/me/  -> Update my profile
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = MedicalProfile.objects.get(user=request.user)
            serializer = MedicalProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MedicalProfile.DoesNotExist:
            return Response(
                {"error": "PROFILE_NOT_FOUND: No profile exists for this user."}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        if MedicalProfile.objects.filter(user=request.user).exists():
            return Response(
                {"error": "PROFILE_EXISTS: A medical profile has already been created for this user."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        print("--- INCOMING FLUTTERFLOW DATA ---")
        print(request.data)
        
        serializer = MedicalProfileSerializer(data=request.data)
        
        if not serializer.is_valid():
            print("--- SERIALIZER REJECTED THE DATA! ---")
            print("EXACT ERRORS:", serializer.errors) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        try:
            profile = MedicalProfile.objects.get(user=request.user)
        except MedicalProfile.DoesNotExist:
            return Response(
                {"error": "PROFILE_NOT_FOUND: Cannot update a profile that does not exist."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # 'partial=True' allows FlutterFlow to update just one or two fields at a time
        serializer = MedicalProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateFCMTokenView(APIView):
    """
    POST /api/v1/profiles/update-fcm-token/ -> Update the user's FCM token for push notifications
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        fcm_token = request.data.get('fcm_token')
        
        if not fcm_token:
            return Response(
                {"error": "FCM_TOKEN_REQUIRED: 'fcm_token' field is required in the request body."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            profile, _ = MedicalProfile.objects.get_or_create(user=request.user)
            profile.fcm_token = fcm_token
            profile.save()
            return Response({"status": "success", "message": "FCM token updated successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred while updating the FCM token: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )