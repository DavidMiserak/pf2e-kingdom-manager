from django.contrib import admin

from .models import (
    ActivityLog,
    Kingdom,
    KingdomMembership,
    KingdomSkillProficiency,
    KingdomTurn,
    LeadershipAssignment,
)


class LeadershipAssignmentInline(admin.TabularInline):
    model = LeadershipAssignment
    extra = 0
    max_num = 8


class KingdomSkillProficiencyInline(admin.TabularInline):
    model = KingdomSkillProficiency
    extra = 0
    max_num = 16


class KingdomTurnInline(admin.TabularInline):
    model = KingdomTurn
    extra = 0
    fields = ["turn_number", "in_game_month", "completed_at"]
    readonly_fields = ["completed_at"]


@admin.register(Kingdom)
class KingdomAdmin(admin.ModelAdmin):
    list_display = ["name", "level", "unrest"]
    search_fields = ["name"]
    inlines = [
        LeadershipAssignmentInline,
        KingdomSkillProficiencyInline,
        KingdomTurnInline,
    ]


@admin.register(KingdomMembership)
class KingdomMembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "kingdom", "role"]
    list_filter = ["role"]


class ActivityLogInline(admin.TabularInline):
    model = ActivityLog
    extra = 0
    fields = ["activity_name", "activity_trait", "performed_by", "degree_of_success"]


@admin.register(KingdomTurn)
class KingdomTurnAdmin(admin.ModelAdmin):
    list_display = ["kingdom", "turn_number", "in_game_month", "completed_at"]
    list_filter = ["kingdom"]
    inlines = [ActivityLogInline]
