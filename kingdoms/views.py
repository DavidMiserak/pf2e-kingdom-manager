import uuid

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView

from kingdoms.constants import AbilityScore
from skills.models import SKILL_KEY_ABILITY

from .forms import CharacterNameForm, KingdomCreateForm, KingdomUpdateForm
from .mixins import GMRequiredMixin, KingdomAccessMixin
from .models import Kingdom, KingdomMembership, MembershipRole
from .url_helpers import kingdom_url


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
        return kingdom_url("kingdom_detail", self.object.pk)


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

        # Group skills and effects by ability for display
        ability_effects = kingdom.get_ability_effects()
        gov_skills = kingdom.government_skill_boosts
        abilities_data = {}
        for ability in AbilityScore:
            skills_for_ability = [
                s
                for s in context["skills"]
                if SKILL_KEY_ABILITY.get(s.skill) == ability
            ]
            for s in skills_for_ability:
                s.government_boosted = s.skill in gov_skills
            abilities_data[ability.label] = {
                "skills": skills_for_ability,
                "effects": ability_effects.get(ability.label, []),
            }
        context["abilities_data"] = abilities_data
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
        return kingdom_url("kingdom_detail", self.object.pk)


class KingdomDeleteView(GMRequiredMixin, TemplateView):
    template_name = "kingdoms/kingdom_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        name = self.kingdom.name
        self.kingdom.delete()
        messages.success(request, f'Kingdom "{name}" has been deleted.')
        return redirect(reverse("kingdoms:kingdom_list"))


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
        return redirect(kingdom_url("kingdom_detail", self.kingdom.pk))


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
        return redirect(kingdom_url("kingdom_detail", kingdom.pk))


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
