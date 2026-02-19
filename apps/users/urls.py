from django.urls import path
from . import views

urlpatterns = [
    # POST /api/v1/users/sync/
    path('sync/', views.UserSyncView.as_view(), name='user-sync'),
    
    # GET /api/v1/users/health/
    path('health/', views.UserHealthView.as_view(), name='user-health'),
]