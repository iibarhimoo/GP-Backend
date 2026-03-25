from django.urls import path
from .views import (
    VitalsIngestionView,
    LiveVitalsView,
    RiskResultIngestionView,
    RiskSummaryView,
    AllRiskEventsView,
    MobileDashboardView,
    DeviceStatusView,
    SupportChatView,
    DailyAnalyticsView,
    WeeklyAnalyticsView,
)

urlpatterns = [
    path('vitals/', VitalsIngestionView.as_view(), name='vitals-ingest'),
    path('risk-results/', RiskResultIngestionView.as_view(), name='risk-results-ingest'),
    path('live-vitals/<str:user_id>/', LiveVitalsView.as_view(), name='vitals-live'),
    path('summary/<str:user_id>/', RiskSummaryView.as_view(), name='risk-results-summary'),
    path('risk-events/', AllRiskEventsView.as_view(), name='all-risk-events'),
    path('dashboard/<str:user_id>/', MobileDashboardView.as_view(), name='mobile-dashboard'),
    path('devices/status/<str:user_id>/', DeviceStatusView.as_view(), name='device-status'),
    path('support/chat/', SupportChatView.as_view(), name='support-chat'),
    path('analytics/daily/<str:user_id>/', DailyAnalyticsView.as_view(), name='analytics-daily'),
    path('analytics/weekly/<str:user_id>/', WeeklyAnalyticsView.as_view(), name='analytics-weekly'),
]