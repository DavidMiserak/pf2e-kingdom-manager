from django.contrib import admin

from .models import LeadershipAssignment


@admin.register(LeadershipAssignment)
class LeadershipAssignmentAdmin(admin.ModelAdmin):
    list_display = ["kingdom", "role", "character_name", "is_vacant"]
    list_filter = ["kingdom", "role"]
