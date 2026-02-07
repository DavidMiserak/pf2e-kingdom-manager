import uuid
from functools import cached_property

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import AbilityScore, KingdomSkill


class MembershipRole(models.TextChoices):
    GM = "gm", "Game Master"
    PLAYER = "player", "Player"


class FameInfamyType(models.TextChoices):
    FAME = "fame", "Fame"
    INFAMY = "infamy", "Infamy"


class Charter(models.TextChoices):
    CONQUEST = "conquest", "Conquest"
    EXPANSION = "expansion", "Expansion"
    EXPLORATION = "exploration", "Exploration"
    GRANT = "grant", "Grant"
    OPEN = "open", "Open"


CHARTER_EFFECTS = {
    Charter.CONQUEST: {"boost": AbilityScore.LOYALTY, "flaw": AbilityScore.CULTURE},
    Charter.EXPANSION: {"boost": AbilityScore.CULTURE, "flaw": AbilityScore.STABILITY},
    Charter.EXPLORATION: {
        "boost": AbilityScore.STABILITY,
        "flaw": AbilityScore.ECONOMY,
    },
    Charter.GRANT: {"boost": AbilityScore.ECONOMY, "flaw": AbilityScore.LOYALTY},
    Charter.OPEN: {"boost": None, "flaw": None},
}


class Government(models.TextChoices):
    DESPOTISM = "despotism", "Despotism"
    FEUDALISM = "feudalism", "Feudalism"
    OLIGARCHY = "oligarchy", "Oligarchy"
    REPUBLIC = "republic", "Republic"
    THAUMOCRACY = "thaumocracy", "Thaumocracy"
    YEOMANRY = "yeomanry", "Yeomanry"


GOVERNMENT_EFFECTS = {
    Government.DESPOTISM: [AbilityScore.STABILITY, AbilityScore.ECONOMY],
    Government.FEUDALISM: [AbilityScore.STABILITY, AbilityScore.CULTURE],
    Government.OLIGARCHY: [AbilityScore.LOYALTY, AbilityScore.ECONOMY],
    Government.REPUBLIC: [AbilityScore.STABILITY, AbilityScore.LOYALTY],
    Government.THAUMOCRACY: [AbilityScore.ECONOMY, AbilityScore.CULTURE],
    Government.YEOMANRY: [AbilityScore.LOYALTY, AbilityScore.CULTURE],
}

GOVERNMENT_SKILLS = {
    Government.DESPOTISM: [KingdomSkill.INTRIGUE, KingdomSkill.WARFARE],
    Government.FEUDALISM: [KingdomSkill.DEFENSE, KingdomSkill.TRADE],
    Government.OLIGARCHY: [KingdomSkill.ARTS, KingdomSkill.INDUSTRY],
    Government.REPUBLIC: [KingdomSkill.ENGINEERING, KingdomSkill.POLITICS],
    Government.THAUMOCRACY: [KingdomSkill.FOLKLORE, KingdomSkill.MAGIC],
    Government.YEOMANRY: [KingdomSkill.AGRICULTURE, KingdomSkill.WILDERNESS],
}


class Heartland(models.TextChoices):
    FOREST_SWAMP = "forest_swamp", "Forest or Swamp"
    HILL_PLAIN = "hill_plain", "Hill or Plain"
    LAKE_RIVER = "lake_river", "Lake or River"
    MOUNTAIN_RUINS = "mountain_ruins", "Mountain or Ruins"


HEARTLAND_EFFECTS = {
    Heartland.FOREST_SWAMP: AbilityScore.CULTURE,
    Heartland.HILL_PLAIN: AbilityScore.LOYALTY,
    Heartland.LAKE_RIVER: AbilityScore.ECONOMY,
    Heartland.MOUNTAIN_RUINS: AbilityScore.STABILITY,
}


# Size category breakpoints: (max_hexes, label, storage_limit, resource_die)
SIZE_CATEGORIES = [
    (9, "Territory", 4, "d4"),
    (24, "Province", 8, "d6"),
    (49, "State", 12, "d8"),
    (99, "Country", 16, "d10"),
    (None, "Dominion", 20, "d12"),
]


class Kingdom(models.Model):
    name = models.CharField(max_length=100)
    invite_code = models.UUIDField(default=uuid.uuid4, unique=True)
    charter = models.CharField(
        max_length=11,
        choices=Charter,
        blank=True,
        default="",
    )
    charter_ability_boost = models.CharField(
        max_length=9,
        choices=AbilityScore,
        blank=True,
        default="",
        help_text="Free ability boost granted by charter (player's choice).",
    )
    government = models.CharField(
        max_length=11,
        choices=Government,
        blank=True,
        default="",
    )
    government_ability_boost = models.CharField(
        max_length=9,
        choices=AbilityScore,
        blank=True,
        default="",
        help_text="Free ability boost granted by government (player's choice).",
    )
    heartland = models.CharField(
        max_length=15,
        choices=Heartland,
        blank=True,
        default="",
    )

    # Ability scores
    culture_score = models.PositiveSmallIntegerField(default=10)
    economy_score = models.PositiveSmallIntegerField(default=10)
    loyalty_score = models.PositiveSmallIntegerField(default=10)
    stability_score = models.PositiveSmallIntegerField(default=10)

    # Level and XP
    level = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
    )
    xp = models.PositiveIntegerField(default=0)

    # Unrest
    unrest = models.PositiveSmallIntegerField(default=0)

    # Fame / Infamy
    fame_points = models.PositiveSmallIntegerField(default=0)
    fame_type = models.CharField(
        max_length=6,
        choices=FameInfamyType,
        default=FameInfamyType.FAME,
    )

    # Resource tracking
    resource_points = models.PositiveIntegerField(default=0)
    bonus_dice = models.PositiveSmallIntegerField(default=0)
    penalty_dice = models.PositiveSmallIntegerField(default=0)

    # Ruin: Corruption (opposes Culture)
    corruption_points = models.PositiveSmallIntegerField(default=0)
    corruption_threshold = models.PositiveSmallIntegerField(default=10)
    corruption_penalty = models.PositiveSmallIntegerField(default=0)

    # Ruin: Crime (opposes Economy)
    crime_points = models.PositiveSmallIntegerField(default=0)
    crime_threshold = models.PositiveSmallIntegerField(default=10)
    crime_penalty = models.PositiveSmallIntegerField(default=0)

    # Ruin: Strife (opposes Loyalty)
    strife_points = models.PositiveSmallIntegerField(default=0)
    strife_threshold = models.PositiveSmallIntegerField(default=10)
    strife_penalty = models.PositiveSmallIntegerField(default=0)

    # Ruin: Decay (opposes Stability)
    decay_points = models.PositiveSmallIntegerField(default=0)
    decay_threshold = models.PositiveSmallIntegerField(default=10)
    decay_penalty = models.PositiveSmallIntegerField(default=0)

    # Size (manual until Phase 3 hex tracking)
    claimed_hexes = models.PositiveSmallIntegerField(default=0)

    # Commodity stockpiles
    food = models.PositiveIntegerField(default=0)
    lumber = models.PositiveIntegerField(default=0)
    ore = models.PositiveIntegerField(default=0)
    stone = models.PositiveIntegerField(default=0)
    luxuries = models.PositiveIntegerField(default=0)

    # Members (M2M through KingdomMembership)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="KingdomMembership",
        related_name="kingdoms",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    # --- Computed properties ---

    @property
    def charter_boost(self):
        if self.charter:
            return CHARTER_EFFECTS[self.charter]["boost"]
        return None

    @property
    def charter_flaw(self):
        if self.charter:
            return CHARTER_EFFECTS[self.charter]["flaw"]
        return None

    @property
    def heartland_boost(self):
        if self.heartland:
            return HEARTLAND_EFFECTS[self.heartland]
        return None

    @property
    def government_boosts(self):
        if self.government:
            return GOVERNMENT_EFFECTS[self.government]
        return []

    @property
    def government_skill_boosts(self):
        """Return set of skill values boosted by government."""
        if self.government:
            return {s.value for s in GOVERNMENT_SKILLS[self.government]}
        return set()

    def get_ability_effects(self):
        """Return per-ability list of boost/flaw sources for display.

        Keyed by ability label (e.g., "Culture") to match template iteration.
        """
        effects = {ability.label: [] for ability in AbilityScore}
        # Charter fixed boost
        if self.charter_boost:
            effects[self.charter_boost.label].append(
                {"source": self.get_charter_display(), "type": "boost", "free": False}
            )
        # Charter free boost
        if self.charter_ability_boost:
            label = AbilityScore(self.charter_ability_boost).label
            effects[label].append(
                {"source": self.get_charter_display(), "type": "boost", "free": True}
            )
        # Charter flaw
        if self.charter_flaw:
            effects[self.charter_flaw.label].append(
                {"source": self.get_charter_display(), "type": "flaw", "free": False}
            )
        # Heartland boost
        if self.heartland_boost:
            effects[self.heartland_boost.label].append(
                {"source": self.get_heartland_display(), "type": "boost", "free": False}
            )
        # Government fixed boosts
        if self.government:
            for ability in self.government_boosts:
                effects[ability.label].append(
                    {
                        "source": self.get_government_display(),
                        "type": "boost",
                        "free": False,
                    }
                )
        # Government free boost
        if self.government_ability_boost:
            label = AbilityScore(self.government_ability_boost).label
            effects[label].append(
                {"source": self.get_government_display(), "type": "boost", "free": True}
            )
        return effects

    @staticmethod
    def _ability_modifier(score):
        return (score - 10) // 2

    @property
    def culture_modifier(self):
        return self._ability_modifier(self.culture_score)

    @property
    def economy_modifier(self):
        return self._ability_modifier(self.economy_score)

    @property
    def loyalty_modifier(self):
        return self._ability_modifier(self.loyalty_score)

    @property
    def stability_modifier(self):
        return self._ability_modifier(self.stability_score)

    def get_ability_modifier(self, ability):
        return self._ability_modifier(getattr(self, f"{ability}_score"))

    @property
    def hex_count(self):
        """Number of claimed hexes. Uses manual field until Phase 3 hex model."""
        return self.claimed_hexes

    @cached_property
    def _size_info(self):
        count = self.hex_count
        for max_hexes, label, storage, die in SIZE_CATEGORIES:
            if max_hexes is None or count <= max_hexes:
                return label, storage, die
        return SIZE_CATEGORIES[-1][1:]  # pragma: no cover

    @property
    def size_category(self):
        return self._size_info[0]

    @property
    def commodity_storage_limit(self):
        return self._size_info[1]

    @property
    def resource_die_type(self):
        return self._size_info[2]

    @property
    def size_modifier(self):
        """Control DC modifier based on hex count."""
        count = self.hex_count
        if count <= 9:
            return 0
        if count <= 24:
            return 1
        if count <= 49:
            return 2
        if count <= 99:
            return 3
        return 4

    @property
    def control_dc(self):
        return 14 + self.level + self.size_modifier

    @property
    def unrest_penalty(self):
        if self.unrest >= 15:
            return -4
        if self.unrest >= 10:
            return -3
        if self.unrest >= 5:
            return -2
        if self.unrest >= 1:
            return -1
        return 0

    def initialize_defaults(self):
        """Create the 8 leadership slots and 16 skill proficiency records."""
        from leadership.models import LeadershipAssignment, LeadershipRole
        from skills.models import KingdomSkillProficiency

        for role in LeadershipRole:
            LeadershipAssignment.objects.get_or_create(kingdom=self, role=role)
        for skill in KingdomSkill:
            KingdomSkillProficiency.objects.get_or_create(kingdom=self, skill=skill)


class KingdomMembership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="kingdom_memberships",
    )
    kingdom = models.ForeignKey(
        Kingdom,
        on_delete=models.CASCADE,
        related_name="kingdom_memberships",
    )
    role = models.CharField(max_length=6, choices=MembershipRole)
    character_name = models.CharField(max_length=100, default="Bilbo")

    class Meta:
        unique_together = [("user", "kingdom")]
        indexes = [
            models.Index(fields=["kingdom", "user"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.kingdom} ({self.get_role_display()})"
