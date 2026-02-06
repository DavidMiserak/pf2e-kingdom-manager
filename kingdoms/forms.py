from django import forms
from django.contrib.auth import get_user_model
from django.forms import modelformset_factory

from .models import (
    ActivityLog,
    Kingdom,
    KingdomMembership,
    KingdomSkillProficiency,
    KingdomTurn,
    LeadershipAssignment,
    MembershipRole,
)

User = get_user_model()


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
            "claimed_hexes",
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

    def __init__(self, *args, kingdom=None, **kwargs):
        super().__init__(*args, **kwargs)
        if kingdom is not None:
            self.fields["user"].queryset = User.objects.filter(kingdoms=kingdom)
        elif self.instance.pk:
            self.fields["user"].queryset = User.objects.filter(
                kingdoms=self.instance.kingdom
            )
        kingdom_for_label = kingdom or (
            self.instance.kingdom if self.instance.pk else None
        )
        if kingdom_for_label:
            names = dict(
                KingdomMembership.objects.filter(kingdom=kingdom_for_label).values_list(
                    "user_id", "character_name"
                )
            )
            self.fields["user"].label_from_instance = lambda u: (
                f"{names.get(u.pk, '')} ({u.email})" if names.get(u.pk) else u.email
            )
        else:
            self.fields["user"].label_from_instance = lambda u: u.email


class LeadershipFormSetBase(
    modelformset_factory(
        LeadershipAssignment,
        form=LeadershipAssignmentForm,
        extra=0,
        max_num=8,
    )
):
    def __init__(self, *args, kingdom=None, **kwargs):
        self.kingdom = kingdom
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["kingdom"] = self.kingdom
        return kwargs


LeadershipFormSet = LeadershipFormSetBase


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


class CharacterNameForm(forms.ModelForm):
    class Meta:
        model = KingdomMembership
        fields = ["character_name"]


class TurnCreateForm(forms.ModelForm):
    class Meta:
        model = KingdomTurn
        fields = ["in_game_month", "starting_rp", "resource_dice_rolled", "notes"]


class TurnUpdateForm(forms.ModelForm):
    class Meta:
        model = KingdomTurn
        fields = [
            "in_game_month",
            "starting_rp",
            "resource_dice_rolled",
            "collected_taxes",
            "improved_lifestyle",
            "tapped_treasury",
            "ending_rp",
            "rp_converted_to_xp",
            "xp_gained",
            "leveled_up",
            "notes",
        ]


class ActivityForm(forms.ModelForm):
    class Meta:
        model = ActivityLog
        fields = [
            "activity_name",
            "activity_trait",
            "skill_used",
            "performed_by",
            "roll_result",
            "total_modifier",
            "dc",
            "degree_of_success",
            "notes",
        ]

    def __init__(self, *args, kingdom=None, membership=None, **kwargs):
        super().__init__(*args, **kwargs)
        if kingdom:
            self.fields["performed_by"].queryset = LeadershipAssignment.objects.filter(
                kingdom=kingdom
            )
            self.fields["performed_by"].label_from_instance = lambda obj: (
                f"{obj.get_role_display()} — {obj.display_name}"
            )
            if (
                membership
                and membership.role == MembershipRole.PLAYER
                and not self.instance.pk
            ):
                user_roles = LeadershipAssignment.objects.filter(
                    kingdom=kingdom, user=membership.user, is_vacant=False
                )
                if user_roles.count() == 1:
                    self.fields["performed_by"].initial = user_roles.first()
