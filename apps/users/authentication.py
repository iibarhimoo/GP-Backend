from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth
from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError, RevokedIdTokenError
from django.contrib.auth import get_user_model

# Always get the custom User model dynamically
User = get_user_model()

def verify_firebase_token(request):
    """Parse and verify a Firebase ID token from the Authorization header."""
    # Support both Django's request.META and DRF's request.headers
    auth_header = request.headers.get('Authorization') or request.META.get('HTTP_AUTHORIZATION')

    if not auth_header:
        raise AuthenticationFailed("No Authorization header provided.")

    parts = auth_header.split()
    if parts[0].lower() != 'bearer':
        raise AuthenticationFailed("Authorization header must start with Bearer.")
    if len(parts) == 1:
        raise AuthenticationFailed("Token missing.")
    if len(parts) > 2:
        raise AuthenticationFailed("Authorization header must be 'Bearer <token>'.")

    token = parts[1]

    try:
        # check_revoked=True forces a check to ensure the user hasn't been disabled in Firebase
        decoded_token = auth.verify_id_token(token, check_revoked=True)
        return decoded_token
        
    except ExpiredIdTokenError:
        raise AuthenticationFailed("FIREBASE_TOKEN_EXPIRED: Please request a new token.")
    except RevokedIdTokenError:
        raise AuthenticationFailed("FIREBASE_TOKEN_REVOKED: User session terminated.")
    except InvalidIdTokenError:
        raise AuthenticationFailed("FIREBASE_TOKEN_INVALID: Invalid token payload.")
    except Exception as e:
        raise AuthenticationFailed(f"Authentication error: {str(e)}")


class FirebaseAuthentication(BaseAuthentication):
    """
    Standard DRF Authentication Class for protected views.
    Requires the user to be valid in Firebase AND exist in the local MySQL database.
    """
    def authenticate(self, request):
        # 1. Use your helper function! If the header is missing, 
        # this will now RAISE an error instead of returning None.
        decoded_token = verify_firebase_token(request)
        uid = decoded_token.get('uid')

        # Strict Statefulness Check
        try:
            # We strictly use .get() here instead of .get_or_create(). 
            # If they hit /profiles/ without calling /sync/ first, we block them.
            user = User.objects.get(username=uid)
            return (user, decoded_token)

        except User.DoesNotExist:
            raise AuthenticationFailed("USER_NOT_SYNCED: User valid in Firebase but not in local DB. Call /api/v1/users/sync/ first.")

    def authenticate_header(self, request):
        return 'Bearer'


class FirebaseAllowUnsyncedAuthentication(BaseAuthentication):
    """
    Permissive DRF Authentication Class ONLY for the onboarding/sync endpoint.
    Validates the Firebase token, but skips the local MySQL user check so new 
    users can successfully register their data.
    """
    def authenticate(self, request):
        decoded_token = verify_firebase_token(request)
        
        # We deliberately DO NOT check User.objects.get() here.
        # We return None for the user object, but pass the decoded_token forward 
        # so your view can extract the UID and create the user in the database.
        return (None, decoded_token)

    def authenticate_header(self, request):
        return 'Bearer'