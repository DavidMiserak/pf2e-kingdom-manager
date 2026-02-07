from django.conf import settings
from django.db import models

from kingdoms.constants import AbilityScore


class LeadershipRole(models.TextChoices):
    RULER = "ruler", "Ruler"
    COUNSELOR = "counselor", "Counselor"
    GENERAL = "general", "General"
    EMISSARY = "emissary", "Emissary"
    MAGISTER = "magister", "Magister"
    TREASURER = "treasurer", "Treasurer"
    VICEROY = "viceroy", "Viceroy"
    WARDEN = "warden", "Warden"


ROLE_KEY_ABILITY = {
    LeadershipRole.RULER: AbilityScore.LOYALTY,
    LeadershipRole.COUNSELOR: AbilityScore.CULTURE,
    LeadershipRole.GENERAL: AbilityScore.STABILITY,
    LeadershipRole.EMISSARY: AbilityScore.LOYALTY,
    LeadershipRole.MAGISTER: AbilityScore.CULTURE,
    LeadershipRole.TREASURER: AbilityScore.ECONOMY,
    LeadershipRole.VICEROY: AbilityScore.ECONOMY,
    LeadershipRole.WARDEN: AbilityScore.STABILITY,
}


class LeadershipAssignment(models.Model):
    kingdom = models.ForeignKey(
        "kingdoms.Kingdom",
        on_delete=models.CASCADE,
        related_name="leadership_assignments",
    )
    role = models.CharField(max_length=10, choices=LeadershipRole)
    character_name = models.CharField(max_length=100, blank=True, default="")
    is_pc = models.BooleanField(default=True)
    is_invested = models.BooleanField(default=False)
    is_vacant = models.BooleanField(default=True)
    downtime_fulfilled = models.BooleanField(default=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leadership_assignments",
    )

    class Meta:
        unique_together = [("kingdom", "role")]
        ordering = ["role"]
        db_table = "kingdoms_leadershipassignment"

    def __str__(self):
        return f"{self.get_role_display()} - {self.character_name or 'Vacant'}"

    @property
    def key_ability(self):
        return ROLE_KEY_ABILITY.get(self.role)

    def get_key_ability_display(self):
        ability = self.key_ability
        return ability.label if ability else ""

    @property
    def status_bonus(self):
        """Investment status bonus based on kingdom level."""
        if not self.is_invested or self.is_vacant:
            return 0
        level = self.kingdom.level
        if level >= 16:
            return 3
        if level >= 8:
            return 2
        return 1

    @property
    def display_name(self):
        """Character name for display: PC membership name or NPC character_name."""
        if self.is_pc and self.user:
            membership = self.kingdom.kingdom_memberships.filter(user=self.user).first()
            if membership:
                return membership.character_name
        return self.character_name
