from django.urls import path
from .views import MyProfileManageView , UpdateFCMTokenView

urlpatterns = [
    # GET, POST, or PUT to /api/v1/profiles/me/
    path('me/', MyProfileManageView.as_view(), name='medical-profile-manage'),
    # POST to /api/v1/profiles/update-fcm-token/
    path('update-fcm-token/', UpdateFCMTokenView.as_view(), name='update-fcm-token'),
]