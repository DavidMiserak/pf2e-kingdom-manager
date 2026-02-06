from django import forms
from django.contrib.auth import get_user_model
from django.forms import modelformset_factory

from .models import (
    CHARTER_EFFECTS,
    GOVERNMENT_EFFECTS,
    GOVERNMENT_SKILLS,
    HEARTLAND_EFFECTS,
    ActivityLog,
    Charter,
    Government,
    Heartland,
    Kingdom,
    KingdomMembership,
    KingdomSkillProficiency,
    KingdomTurn,
    LeadershipAssignment,
    MembershipRole,
)

User = get_user_model()


def _charter_choices(*, include_blank=True):
    """Build charter choices with boost/flaw labels."""
    choices = [("", "None" if not include_blank else "---------")]
    for charter in Charter:
        effects = CHARTER_EFFECTS[charter]
        parts = []
        if effects["boost"]:
            parts.append(f"+{effects['boost'].label}")
        if effects["flaw"]:
            parts.append(f"\u2212{effects['flaw'].label}")
        suffix = f" ({', '.join(parts)})" if parts else ""
        choices.append((charter.value, f"{charter.label}{suffix}"))
    return choices


def _heartland_choices(*, include_blank=True):
    """Build heartland choices with boost labels."""
    choices = [("", "None" if not include_blank else "---------")]
    for heartland in Heartland:
        boost = HEARTLAND_EFFECTS[heartland]
        choices.append((heartland.value, f"{heartland.label} (+{boost.label})"))
    return choices


def _government_choices(*, include_blank=True):
    """Build government choices with boost and skill labels."""
    choices = [("", "None" if not include_blank else "---------")]
    for gov in Government:
        boosts = GOVERNMENT_EFFECTS[gov]
        skills = GOVERNMENT_SKILLS[gov]
        boost_str = ", ".join(f"+{b.label}" for b in boosts)
        skill_str = ", ".join(s.label for s in skills)
        choices.append((gov.value, f"{gov.label} ({boost_str}; {skill_str})"))
    return choices


class KingdomCreateForm(forms.ModelForm):
    class Meta:
        model = Kingdom
        fields = [
            "name",
            "charter",
            "charter_ability_boost",
            "heartland",
            "government",
            "government_ability_boost",
            "fame_type",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["charter"].choices = _charter_choices()
        self.fields["heartland"].choices = _heartland_choices()
        self.fields["government"].choices = _government_choices()


class KingdomUpdateForm(forms.ModelForm):
    class Meta:
        model = Kingdom
        fields = [
            "name",
            "charter",
            "charter_ability_boost",
            "heartland",
            "government",
            "government_ability_boost",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["charter"].choices = _charter_choices(include_blank=False)
        self.fields["heartland"].choices = _heartland_choices(include_blank=False)
        self.fields["government"].choices = _government_choices(include_blank=False)


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
            "event_occurred",
            "event_xp",
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
