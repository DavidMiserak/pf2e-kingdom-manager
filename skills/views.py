from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from kingdoms.mixins import GMRequiredMixin

from .forms import SkillProficiencyFormSet


class SkillsUpdateView(GMRequiredMixin, TemplateView):
    template_name = "kingdoms/skills_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "formset" not in kwargs:
            context["formset"] = SkillProficiencyFormSet(
                queryset=self.kingdom.skill_proficiencies.all()
            )
        gov_skills = self.kingdom.government_skill_boosts
        for form in context["formset"]:
            form.government_boosted = form.instance.skill in gov_skills
        return context

    def post(self, request, *args, **kwargs):
        formset = SkillProficiencyFormSet(
            request.POST,
            queryset=self.kingdom.skill_proficiencies.all(),
        )
        if formset.is_valid():
            formset.save()
            messages.success(request, "Skill proficiencies updated.")
            return redirect(
                reverse(
                    "kingdoms:kingdom_detail",
                    kwargs={"pk": self.kingdom.pk},
                )
            )
        return self.render_to_response(self.get_context_data(formset=formset))
