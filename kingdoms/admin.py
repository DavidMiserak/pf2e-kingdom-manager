from django.contrib import admin

from .models import (
    Kingdom,
    KingdomMembership,
    KingdomSkillProficiency,
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


@admin.register(Kingdom)
class KingdomAdmin(admin.ModelAdmin):
    list_display = ["name", "level", "unrest"]
    search_fields = ["name"]
    inlines = [LeadershipAssignmentInline, KingdomSkillProficiencyInline]


@admin.register(KingdomMembership)
class KingdomMembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "kingdom", "role"]
    list_filter = ["role"]
