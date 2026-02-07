from django.contrib import admin

from .models import KingdomSkillProficiency


@admin.register(KingdomSkillProficiency)
class KingdomSkillProficiencyAdmin(admin.ModelAdmin):
    list_display = ["kingdom", "skill", "proficiency"]
    list_filter = ["kingdom", "proficiency"]
