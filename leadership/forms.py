from django import forms
from django.contrib.auth import get_user_model
from django.forms import modelformset_factory

from kingdoms.models import KingdomMembership

from .models import LeadershipAssignment

User = get_user_model()


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
