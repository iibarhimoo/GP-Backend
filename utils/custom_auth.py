import os
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class StaticAPIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # DRF's bulletproof way to safely grab the header
        auth_header = get_authorization_header(request).decode('utf-8')
        
        if not auth_header:
            return None # Move on to Firebase Auth if no header exists

        # Extract the token
        token = auth_header.replace("Bearer ", "").strip()
        expected_n8n_token = os.environ.get('N8N_MASTER_TOKEN', 'amer_local_test_key')
        expected_eyad_token = os.environ.get('EYAD_TEST_TOKEN', 'eyad_local_test_key')

        # 1. N8N Service Account (Amer)
        if token == expected_n8n_token:
            user, _ = User.objects.get_or_create(username="n8n_service_account")
            user.is_staff = True 
            return (user, "StaticToken")

        # 2. Eyad Test Account
        if token == expected_eyad_token:
            user, _ = User.objects.get_or_create(username="S10") 
            user.is_staff = False
            return (user, "StaticToken")

        # If it has a header but it doesn't match our static keys, let Firebase try it!
        return None