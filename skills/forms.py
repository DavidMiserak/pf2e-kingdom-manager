from django import forms
from django.forms import modelformset_factory

from .models import KingdomSkillProficiency


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
