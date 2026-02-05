from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from .models import Kingdom, KingdomMembership, MembershipRole


class KingdomAccessMixin(LoginRequiredMixin):
    """Verify user is a member of the kingdom referenced by URL pk."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            self.kingdom = Kingdom.objects.get(pk=self.kwargs["pk"])
        except Kingdom.DoesNotExist:
            raise Http404
        try:
            self.membership = KingdomMembership.objects.get(
                user=request.user, kingdom=self.kingdom
            )
        except KingdomMembership.DoesNotExist:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["kingdom"] = self.kingdom
        context["membership"] = self.membership
        context["is_gm"] = self.membership.role == MembershipRole.GM
        return context


class GMRequiredMixin(KingdomAccessMixin):
    """Verify user is a GM of the kingdom."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            self.kingdom = Kingdom.objects.get(pk=self.kwargs["pk"])
        except Kingdom.DoesNotExist:
            raise Http404
        try:
            self.membership = KingdomMembership.objects.get(
                user=request.user, kingdom=self.kingdom
            )
        except KingdomMembership.DoesNotExist:
            raise Http404
        if self.membership.role != MembershipRole.GM:
            raise Http404
        # Skip KingdomAccessMixin.dispatch to avoid duplicate lookups
        return LoginRequiredMixin.dispatch(self, request, *args, **kwargs)
