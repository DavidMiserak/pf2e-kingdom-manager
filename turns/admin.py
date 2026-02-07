from django.contrib import admin

from .models import ActivityLog, KingdomTurn


class ActivityLogInline(admin.TabularInline):
    model = ActivityLog
    extra = 0
    fields = ["activity_name", "activity_trait", "performed_by", "degree_of_success"]


@admin.register(KingdomTurn)
class KingdomTurnAdmin(admin.ModelAdmin):
    list_display = ["kingdom", "turn_number", "in_game_month", "completed_at"]
    list_filter = ["kingdom"]
    inlines = [ActivityLogInline]
