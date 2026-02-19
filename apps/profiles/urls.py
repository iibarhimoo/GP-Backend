from django.urls import path
from .views import MyProfileManageView

urlpatterns = [
    # GET, POST, or PUT to /api/v1/profiles/me/
    path('me/', MyProfileManageView.as_view(), name='medical-profile-manage'),
]