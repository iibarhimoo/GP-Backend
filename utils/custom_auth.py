import os
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User

class StaticAPIKeyAuthentication(BaseAuthentication):
    """
    Allows n8n (Amer) and Swagger/Postman (Eyad) to bypass Firebase 
    using static, never-expiring API tokens.
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None # Move on to Firebase Auth if no header exists

        # Extract the token (handles "Bearer <token>" or just "<token>")
        token = auth_header.replace("Bearer ", "").strip()
        print(f"--- INCOMING TOKEN SEEN BY DJANGO '{token}' ---") # Debug print to confirm token reception
        # 1. N8N Service Account (Amer)
        if token == os.environ.get('N8N_MASTER_TOKEN', 'amer_local_test_key'):
            # Get or create a dummy user for the server pipeline
            user, _ = User.objects.get_or_create(username="n8n_service_account")
            user.is_staff = True # Grant admin privileges so Amer can push data for ANY user (S10, S11, etc.)
            return (user, "StaticToken")

        # 2. Eyad Test Account
        if token == os.environ.get('EYAD_TEST_TOKEN', 'eyad_local_test_key'):
            # Eyad acts as the subject 'S10' to test standard mobile fetching
            user, _ = User.objects.get_or_create(username="S10") 
            user.is_staff = False
            return (user, "StaticToken")

        # If the token doesn't match these two, return None so Firebase Auth can try to decode it
        return None