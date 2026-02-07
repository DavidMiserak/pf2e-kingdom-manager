from django.contrib import admin

from leadership.models import LeadershipAssignment
from skills.models import KingdomSkillProficiency
from turns.models import KingdomTurn

from .models import Kingdom, KingdomMembership


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
