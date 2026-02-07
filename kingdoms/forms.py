from django import forms

from .models import (
    CHARTER_EFFECTS,
    GOVERNMENT_EFFECTS,
    GOVERNMENT_SKILLS,
    HEARTLAND_EFFECTS,
    Charter,
    Government,
    Heartland,
    Kingdom,
    KingdomMembership,
)


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


class CharacterNameForm(forms.ModelForm):
    class Meta:
        model = KingdomMembership
        fields = ["character_name"]
