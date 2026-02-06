import uuid
from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView

from .forms import (
    ActivityForm,
    CharacterNameForm,
    KingdomCreateForm,
    KingdomUpdateForm,
    LeadershipFormSet,
    SkillProficiencyFormSet,
    TurnCreateForm,
    TurnUpdateForm,
)
from .mixins import GMRequiredMixin, KingdomAccessMixin
from .models import (
    SKILL_KEY_ABILITY,
    AbilityScore,
    ActivityLog,
    Kingdom,
    KingdomMembership,
    KingdomTurn,
    MembershipRole,
)


class KingdomListView(LoginRequiredMixin, ListView):
    model = Kingdom
    template_name = "kingdoms/kingdom_list.html"
    context_object_name = "kingdoms"

    def get_queryset(self):
        return Kingdom.objects.filter(members=self.request.user)


class KingdomCreateView(LoginRequiredMixin, CreateView):
    model = Kingdom
    form_class = KingdomCreateForm
    template_name = "kingdoms/kingdom_form.html"

    def form_valid(self, form):
        self.object = form.save()
        self.object.initialize_defaults()
        KingdomMembership.objects.create(
            user=self.request.user,
            kingdom=self.object,
            role=MembershipRole.GM,
        )
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("kingdoms:kingdom_detail", kwargs={"pk": self.object.pk})


class KingdomDetailView(KingdomAccessMixin, DetailView):
    model = Kingdom
    template_name = "kingdoms/kingdom_detail.html"
    context_object_name = "kingdom"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kingdom = self.object
        context["leadership"] = kingdom.leadership_assignments.all()
        context["skills"] = kingdom.skill_proficiencies.all()
        context["memberships"] = kingdom.kingdom_memberships.select_related(
            "user"
        ).all()

        # Group skills by ability for display
        skills_by_ability = {}
        for ability in AbilityScore:
            skills_by_ability[ability.label] = [
                s
                for s in context["skills"]
                if SKILL_KEY_ABILITY.get(s.skill) == ability
            ]
        context["skills_by_ability"] = skills_by_ability
        context["character_name_form"] = CharacterNameForm(instance=self.membership)

        # Recent turns
        context["turns"] = kingdom.turns.all()[:5]
        context["current_turn"] = kingdom.turns.filter(
            completed_at__isnull=True
        ).first()
        return context


class KingdomUpdateView(GMRequiredMixin, UpdateView):
    model = Kingdom
    form_class = KingdomUpdateForm
    template_name = "kingdoms/kingdom_update.html"

    def get_success_url(self):
        return reverse("kingdoms:kingdom_detail", kwargs={"pk": self.object.pk})


class KingdomDeleteView(GMRequiredMixin, TemplateView):
    template_name = "kingdoms/kingdom_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        name = self.kingdom.name
        self.kingdom.delete()
        messages.success(request, f'Kingdom "{name}" has been deleted.')
        return redirect(reverse("kingdoms:kingdom_list"))


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


class SkillsUpdateView(GMRequiredMixin, TemplateView):
    template_name = "kingdoms/skills_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "formset" not in kwargs:
            context["formset"] = SkillProficiencyFormSet(
                queryset=self.kingdom.skill_proficiencies.all()
            )
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


class KingdomMemberManageView(GMRequiredMixin, TemplateView):
    template_name = "kingdoms/member_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["memberships"] = self.kingdom.kingdom_memberships.select_related(
            "user"
        ).all()
        invite_url = self.request.build_absolute_uri(
            reverse(
                "kingdoms:join",
                kwargs={"invite_code": self.kingdom.invite_code},
            )
        )
        context["invite_url"] = invite_url
        return context

    def post(self, request, *args, **kwargs):
        membership_id = request.POST.get("membership_id")
        membership = get_object_or_404(
            KingdomMembership,
            pk=membership_id,
            kingdom=self.kingdom,
        )
        if membership.user == request.user:
            messages.error(request, "You cannot remove yourself.")
        else:
            membership.delete()
            messages.success(request, "Member removed.")
        return redirect(
            reverse(
                "kingdoms:member_manage",
                kwargs={"pk": self.kingdom.pk},
            )
        )


class UpdateCharacterNameView(KingdomAccessMixin, View):
    def post(self, request, *args, **kwargs):
        form = CharacterNameForm(request.POST, instance=self.membership)
        if form.is_valid():
            form.save()
            messages.success(request, "Character name updated.")
        return redirect(
            reverse("kingdoms:kingdom_detail", kwargs={"pk": self.kingdom.pk})
        )


class JoinKingdomView(LoginRequiredMixin, View):
    def get(self, request, invite_code):
        kingdom = get_object_or_404(Kingdom, invite_code=invite_code)
        _, created = KingdomMembership.objects.get_or_create(
            user=request.user,
            kingdom=kingdom,
            defaults={"role": MembershipRole.PLAYER},
        )
        if created:
            messages.success(request, f"You joined {kingdom.name}!")
        else:
            messages.info(request, f"You are already a member of {kingdom.name}.")
        return redirect(reverse("kingdoms:kingdom_detail", kwargs={"pk": kingdom.pk}))


class RegenerateInviteView(GMRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        self.kingdom.invite_code = uuid.uuid4()
        self.kingdom.save(update_fields=["invite_code"])
        messages.success(request, "Invite link regenerated. Old links are now invalid.")
        return redirect(
            reverse(
                "kingdoms:member_manage",
                kwargs={"pk": self.kingdom.pk},
            )
        )


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
        return reverse(
            "kingdoms:turn_detail",
            kwargs={"pk": self.kingdom.pk, "turn_pk": self.object.pk},
        )


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
        return reverse(
            "kingdoms:turn_detail",
            kwargs={"pk": self.kingdom.pk, "turn_pk": self.object.pk},
        )


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
        return redirect(
            reverse("kingdoms:kingdom_detail", kwargs={"pk": self.kingdom.pk})
        )


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
                "kingdoms:turn_detail",
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
                    "kingdoms:turn_detail",
                    kwargs={"pk": self.kingdom.pk, "turn_pk": self.turn.pk},
                )
            )
        form.instance.kingdom = self.kingdom
        form.instance.turn = self.turn
        form.instance.created_by = self.request.user
        # Auto-calculate degree of success if roll data provided and not manually set
        if not form.instance.degree_of_success:
            calculated = form.instance.calculate_degree_of_success()
            if calculated:
                form.instance.degree_of_success = calculated
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "kingdoms:turn_detail",
            kwargs={"pk": self.kingdom.pk, "turn_pk": self.turn.pk},
        )


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
        is_gm = self.membership.role == MembershipRole.GM
        is_creator = self.activity_obj.created_by == request.user
        if not (is_gm or is_creator):
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
        if not form.instance.degree_of_success:
            calculated = form.instance.calculate_degree_of_success()
            if calculated:
                form.instance.degree_of_success = calculated
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "kingdoms:turn_detail",
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
        is_gm = self.membership.role == MembershipRole.GM
        is_creator = activity.created_by == request.user
        if not (is_gm or is_creator):
            raise Http404
        turn_pk = activity.turn.pk
        activity.delete()
        messages.success(request, "Activity deleted.")
        return redirect(
            reverse(
                "kingdoms:turn_detail",
                kwargs={"pk": self.kingdom.pk, "turn_pk": turn_pk},
            )
        )
