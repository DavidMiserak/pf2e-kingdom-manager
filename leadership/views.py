from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from kingdoms.mixins import GMRequiredMixin

from .forms import LeadershipFormSet


class LeadershipUpdateView(GMRequiredMixin, TemplateView):
    template_name = "kingdoms/leadership_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = LeadershipFormSet(
            queryset=self.kingdom.leadership_assignments.all(),
            kingdom=self.kingdom,
        )
        return context

    def post(self, request, *args, **kwargs):
        formset = LeadershipFormSet(
            request.POST,
            queryset=self.kingdom.leadership_assignments.all(),
            kingdom=self.kingdom,
        )
        if formset.is_valid():
            formset.save()
            messages.success(request, "Leadership roles updated.")
            return redirect(
                reverse(
                    "kingdoms:kingdom_detail",
                    kwargs={"pk": self.kingdom.pk},
                )
            )
        return self.render_to_response(self.get_context_data(formset=formset))
