from django.urls import path
from .views import UserSyncView

urlpatterns = [
    path('sync', UserSyncView.as_view(), name='user-sync'),
]