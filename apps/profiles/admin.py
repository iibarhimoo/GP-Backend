from django.contrib import admin
from .models import MedicalProfile

@admin.register(MedicalProfile)
class MedicalProfileAdmin(admin.ModelAdmin):
    # This controls what columns you see in the list
    list_display = ('user', 'height', 'weight', 'dob', 'created_at')
    
    # This allows you to search by email in the admin bar
    search_fields = ('user__email', 'user__username')
    
    # This adds a filter sidebar for dates
    list_filter = ('created_at',)