from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.base import TemplateView

from kingdoms.mixins import GMRequiredMixin, KingdomAccessMixin
from kingdoms.models import Kingdom, KingdomMembership, MembershipRole
from kingdoms.url_helpers import kingdom_url, turn_url

from .forms import ActivityForm, TurnCreateForm, TurnUpdateForm
from .models import ActivityLog, KingdomTurn

# --- Turn views ---


class TurnCreateView(GMRequiredMixin, CreateView):
    model = KingdomTurn
    form_class = TurnCreateForm
    template_name = "kingdoms/turn_form.html"

    def form_valid(self, form):
        form.instance.kingdom = self.kingdom
        last_turn = self.kingdom.turns.first()
        form.instance.turn_number = (last_turn.turn_number + 1) if last_turn else 1
        return super().form_valid(form)

    def get_success_url(self):
        return turn_url("turn_detail", self.kingdom.pk, self.object.pk)


class TurnDetailView(KingdomAccessMixin, DetailView):
    model = KingdomTurn
    template_name = "kingdoms/turn_detail.html"
    context_object_name = "turn"
    pk_url_kwarg = "turn_pk"

    def get_queryset(self):
        return KingdomTurn.objects.filter(kingdom_id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activities = self.object.activities.select_related("performed_by").all()
        context["activities"] = activities
        activities_by_trait = defaultdict(list)
        for activity in activities:
            activities_by_trait[activity.get_activity_trait_display()].append(activity)
        context["activities_by_trait"] = dict(activities_by_trait)
        return context


class TurnUpdateView(GMRequiredMixin, UpdateView):
    model = KingdomTurn
    form_class = TurnUpdateForm
    template_name = "kingdoms/turn_form.html"
    pk_url_kwarg = "turn_pk"

    def get_queryset(self):
        return KingdomTurn.objects.filter(kingdom_id=self.kwargs["pk"])

    def get_success_url(self):
        return turn_url("turn_detail", self.kingdom.pk, self.object.pk)


class TurnDeleteView(GMRequiredMixin, TemplateView):
    template_name = "kingdoms/turn_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["turn"] = get_object_or_404(
            KingdomTurn, pk=self.kwargs["turn_pk"], kingdom=self.kingdom
        )
        return context

    def post(self, request, *args, **kwargs):
        turn = get_object_or_404(
            KingdomTurn, pk=self.kwargs["turn_pk"], kingdom=self.kingdom
        )
        turn_number = turn.turn_number
        turn.delete()
        messages.success(request, f"Turn {turn_number} has been deleted.")
        return redirect(kingdom_url("kingdom_detail", self.kingdom.pk))


class TurnCompleteView(GMRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        turn = get_object_or_404(
            KingdomTurn, pk=self.kwargs["turn_pk"], kingdom=self.kingdom
        )
        if turn.is_complete:
            messages.warning(request, "Turn is already complete.")
        else:
            turn.complete_turn()
            messages.success(request, f"Turn {turn.turn_number} marked as complete.")
        return redirect(
            reverse(
                "turns:turn_detail",
                kwargs={"pk": self.kingdom.pk, "turn_pk": turn.pk},
            )
        )


# --- Activity views ---


class ActivityCreateView(KingdomAccessMixin, CreateView):
    model = ActivityLog
    form_class = ActivityForm
    template_name = "kingdoms/activity_form.html"

    def dispatch(self, request, *args, **kwargs):
        # Set turn BEFORE super().dispatch() which triggers form processing
        try:
            self.turn = KingdomTurn.objects.get(
                pk=kwargs["turn_pk"], kingdom_id=kwargs["pk"]
            )
        except KingdomTurn.DoesNotExist:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["kingdom"] = self.kingdom
        kwargs["membership"] = self.membership
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["turn"] = self.turn
        return context

    def form_valid(self, form):
        if self.turn.is_complete and self.membership.role != MembershipRole.GM:
            messages.error(self.request, "Cannot add activities to a completed turn.")
            return redirect(
                reverse(
                    "turns:turn_detail",
                    kwargs={"pk": self.kingdom.pk, "turn_pk": self.turn.pk},
                )
            )
        form.instance.kingdom = self.kingdom
        form.instance.turn = self.turn
        form.instance.created_by = self.request.user
        # Auto-calculate degree of success if roll data provided and not manually set
        form.instance.auto_populate_degree_of_success()
        return super().form_valid(form)

    def get_success_url(self):
        return turn_url("turn_detail", self.kingdom.pk, self.turn.pk)


class ActivityUpdateView(KingdomAccessMixin, UpdateView):
    model = ActivityLog
    form_class = ActivityForm
    template_name = "kingdoms/activity_form.html"
    pk_url_kwarg = "activity_pk"

    def get_queryset(self):
        return ActivityLog.objects.filter(kingdom_id=self.kwargs["pk"])

    def dispatch(self, request, *args, **kwargs):
        # Duplicate lookup to check creator/GM before super processes form.
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            self.kingdom = Kingdom.objects.get(pk=kwargs["pk"])
        except Kingdom.DoesNotExist:
            raise Http404
        try:
            self.membership = KingdomMembership.objects.get(
                user=request.user, kingdom=self.kingdom
            )
        except KingdomMembership.DoesNotExist:
            raise Http404
        try:
            self.activity_obj = ActivityLog.objects.select_related("turn").get(
                pk=kwargs["activity_pk"], kingdom=self.kingdom
            )
        except ActivityLog.DoesNotExist:
            raise Http404
        if not self.activity_obj.can_be_modified_by(request.user, self.membership):
            raise Http404
        # Skip KingdomAccessMixin.dispatch to avoid duplicate lookups
        return LoginRequiredMixin.dispatch(self, request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["kingdom"] = self.kingdom
        kwargs["membership"] = self.membership
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["turn"] = self.object.turn
        return context

    def form_valid(self, form):
        form.instance.auto_populate_degree_of_success()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "turns:turn_detail",
            kwargs={
                "pk": self.kingdom.pk,
                "turn_pk": self.object.turn.pk,
            },
        )


class ActivityDeleteView(KingdomAccessMixin, View):
    def post(self, request, *args, **kwargs):
        activity = get_object_or_404(
            ActivityLog, pk=self.kwargs["activity_pk"], kingdom=self.kingdom
        )
        if not activity.can_be_modified_by(request.user, self.membership):
            raise Http404
        turn_pk = activity.turn.pk
        activity.delete()
        messages.success(request, "Activity deleted.")
        return redirect(
            reverse(
                "turns:turn_detail",
                kwargs={"pk": self.kingdom.pk, "turn_pk": turn_pk},
            )
        )
