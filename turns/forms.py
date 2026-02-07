from django import forms

from kingdoms.models import MembershipRole
from leadership.models import LeadershipAssignment

from .models import ActivityLog, KingdomTurn


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
