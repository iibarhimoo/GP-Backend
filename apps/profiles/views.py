from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions
from .models import MedicalProfile
from .serializers import MedicalProfileSerializer

class ProfileCreateView(generics.CreateAPIView):
    """
    POST /api/v1/profiles
    Auto-assigns the authenticated user.
    """
    queryset = MedicalProfile.objects.all()
    serializer_class = MedicalProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # 🛑 THE FIX: Check if a profile already exists for this user!
        if MedicalProfile.objects.filter(user=request.user).exists():
            return Response(
                {"error": "PROFILE_EXISTS: A medical profile has already been created for this user."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        print("--- INCOMING FLUTTERFLOW DATA ---")
        print(request.data)
        
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            print("--- SERIALIZER REJECTED THE DATA! ---")
            print("EXACT ERRORS:", serializer.errors) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)