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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)