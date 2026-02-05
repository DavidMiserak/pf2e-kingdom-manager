from django import forms
from django.forms import modelformset_factory

from .models import (
    Kingdom,
    KingdomSkillProficiency,
    LeadershipAssignment,
)


class KingdomCreateForm(forms.ModelForm):
    class Meta:
        model = Kingdom
        fields = ["name", "fame_type"]


class KingdomUpdateForm(forms.ModelForm):
    class Meta:
        model = Kingdom
        fields = [
            "name",
            "culture_score",
            "economy_score",
            "loyalty_score",
            "stability_score",
            "level",
            "xp",
            "unrest",
            "fame_points",
            "fame_type",
            "resource_points",
            "bonus_dice",
            "penalty_dice",
            "corruption_points",
            "corruption_threshold",
            "corruption_penalty",
            "crime_points",
            "crime_threshold",
            "crime_penalty",
            "strife_points",
            "strife_threshold",
            "strife_penalty",
            "decay_points",
            "decay_threshold",
            "decay_penalty",
            "food",
            "lumber",
            "ore",
            "stone",
            "luxuries",
        ]


class LeadershipAssignmentForm(forms.ModelForm):
    class Meta:
        model = LeadershipAssignment
        fields = [
            "character_name",
            "is_pc",
            "is_invested",
            "is_vacant",
            "downtime_fulfilled",
            "user",
        ]


LeadershipFormSet = modelformset_factory(
    LeadershipAssignment,
    form=LeadershipAssignmentForm,
    extra=0,
    max_num=8,
)


class KingdomSkillProficiencyForm(forms.ModelForm):
    class Meta:
        model = KingdomSkillProficiency
        fields = ["proficiency"]


SkillProficiencyFormSet = modelformset_factory(
    KingdomSkillProficiency,
    form=KingdomSkillProficiencyForm,
    extra=0,
    max_num=16,
)
