from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from firebase_admin import auth
from django.contrib.auth import get_user_model

User = get_user_model()

# ---------------------------------------------------------------------------
# 1. THE UTILITY FUNCTION (What you provided, slightly hardened)
# Used explicitly by the /sync endpoint to extract UID before User exists.
# ---------------------------------------------------------------------------
def verify_firebase_token(request):
    """
    Parses and verifies the Firebase ID Token from the Authorization header.
    Returns: The decoded token dictionary (containing 'uid', 'email', etc.)
    Raises: AuthenticationFailed if token is invalid or missing.
    """
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        raise exceptions.AuthenticationFailed("No Authorization header provided.")

    parts = auth_header.split()
    
    if parts[0].lower() != "bearer":
        raise exceptions.AuthenticationFailed("Authorization header must start with Bearer.")
        
    if len(parts) == 1:
        raise exceptions.AuthenticationFailed("Token missing.")
        
    if len(parts) > 2:
        raise exceptions.AuthenticationFailed("Authorization header must be Bearer <token>.")

    token = parts[1]
    
    try:
        # Verify signature, expiry, and project ID
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise exceptions.AuthenticationFailed(f"Invalid Firebase Token: {str(e)}")


# ---------------------------------------------------------------------------
# 2. THE AUTHENTICATION CLASS (The DRF Standard)
# Used automatically by 'IsAuthenticated' permissions on protected views.
# ---------------------------------------------------------------------------
class FirebaseAuthentication(BaseAuthentication):
    """
    Django REST Framework Authentication Class.
    1. Verifies the token using the utility above.
    2. Matches the Firebase UID to a local MySQL User.
    """
    def authenticate(self, request):
        try:
            # Re-use the utility function to get the token data
            decoded_token = verify_firebase_token(request)
            uid = decoded_token.get("uid")
        except exceptions.AuthenticationFailed:
            # If token is bad, return None to let other auth classes try
            # or let the Permission class fail the request.
            return None

        # Statefulness Check: Does this user exist in our MySQL DB?
        try:
            # We map Firebase UID -> Django Username
            user = User.objects.get(username=uid)
            return (user, None)  # Authentication Successful
        except User.DoesNotExist:
            # Token is valid, but User is not in MySQL.
            # This happens if they signed up on Firebase but didn't call /sync.
            raise exceptions.AuthenticationFailed("User valid in Firebase but not synced to local DB. Call /api/v1/auth/sync/ first.")