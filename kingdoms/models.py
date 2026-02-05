import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class AbilityScore(models.TextChoices):
    CULTURE = "culture", "Culture"
    ECONOMY = "economy", "Economy"
    LOYALTY = "loyalty", "Loyalty"
    STABILITY = "stability", "Stability"


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


class Proficiency(models.TextChoices):
    UNTRAINED = "untrained", "Untrained"
    TRAINED = "trained", "Trained"
    EXPERT = "expert", "Expert"
    MASTER = "master", "Master"
    LEGENDARY = "legendary", "Legendary"


PROFICIENCY_BONUS = {
    Proficiency.UNTRAINED: 0,
    Proficiency.TRAINED: 2,
    Proficiency.EXPERT: 4,
    Proficiency.MASTER: 6,
    Proficiency.LEGENDARY: 8,
}


class KingdomSkill(models.TextChoices):
    AGRICULTURE = "agriculture", "Agriculture"
    ARTS = "arts", "Arts"
    BOATING = "boating", "Boating"
    DEFENSE = "defense", "Defense"
    ENGINEERING = "engineering", "Engineering"
    EXPLORATION = "exploration", "Exploration"
    FOLKLORE = "folklore", "Folklore"
    INDUSTRY = "industry", "Industry"
    INTRIGUE = "intrigue", "Intrigue"
    MAGIC = "magic", "Magic"
    POLITICS = "politics", "Politics"
    SCHOLARSHIP = "scholarship", "Scholarship"
    STATECRAFT = "statecraft", "Statecraft"
    TRADE = "trade", "Trade"
    WARFARE = "warfare", "Warfare"
    WILDERNESS = "wilderness", "Wilderness"


SKILL_KEY_ABILITY = {
    KingdomSkill.AGRICULTURE: AbilityScore.LOYALTY,
    KingdomSkill.ARTS: AbilityScore.CULTURE,
    KingdomSkill.BOATING: AbilityScore.ECONOMY,
    KingdomSkill.DEFENSE: AbilityScore.STABILITY,
    KingdomSkill.ENGINEERING: AbilityScore.STABILITY,
    KingdomSkill.EXPLORATION: AbilityScore.ECONOMY,
    KingdomSkill.FOLKLORE: AbilityScore.CULTURE,
    KingdomSkill.INDUSTRY: AbilityScore.ECONOMY,
    KingdomSkill.INTRIGUE: AbilityScore.LOYALTY,
    KingdomSkill.MAGIC: AbilityScore.CULTURE,
    KingdomSkill.POLITICS: AbilityScore.LOYALTY,
    KingdomSkill.SCHOLARSHIP: AbilityScore.CULTURE,
    KingdomSkill.STATECRAFT: AbilityScore.LOYALTY,
    KingdomSkill.TRADE: AbilityScore.ECONOMY,
    KingdomSkill.WARFARE: AbilityScore.LOYALTY,
    KingdomSkill.WILDERNESS: AbilityScore.STABILITY,
}


class MembershipRole(models.TextChoices):
    GM = "gm", "Game Master"
    PLAYER = "player", "Player"


class FameInfamyType(models.TextChoices):
    FAME = "fame", "Fame"
    INFAMY = "infamy", "Infamy"


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
        """Number of claimed hexes. Returns 0 until hex model exists."""
        if hasattr(self, "hex_set"):
            return self.hex_set.filter(status="claimed").count()
        return 0

    def _size_info(self):
        count = self.hex_count
        for max_hexes, label, storage, die in SIZE_CATEGORIES:
            if max_hexes is None or count <= max_hexes:
                return label, storage, die
        return SIZE_CATEGORIES[-1][1:]  # pragma: no cover

    @property
    def size_category(self):
        return self._size_info()[0]

    @property
    def commodity_storage_limit(self):
        return self._size_info()[1]

    @property
    def resource_die_type(self):
        return self._size_info()[2]

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
        for role in LeadershipRole:
            LeadershipAssignment.objects.get_or_create(kingdom=self, role=role)
        for skill in KingdomSkill:
            KingdomSkillProficiency.objects.get_or_create(kingdom=self, skill=skill)


class LeadershipAssignment(models.Model):
    kingdom = models.ForeignKey(
        Kingdom,
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

    def __str__(self):
        return f"{self.get_role_display()} - {self.character_name or 'Vacant'}"

    @property
    def key_ability(self):
        return ROLE_KEY_ABILITY.get(self.role)

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


class KingdomSkillProficiency(models.Model):
    kingdom = models.ForeignKey(
        Kingdom,
        on_delete=models.CASCADE,
        related_name="skill_proficiencies",
    )
    skill = models.CharField(max_length=12, choices=KingdomSkill)
    proficiency = models.CharField(
        max_length=10,
        choices=Proficiency,
        default=Proficiency.UNTRAINED,
    )

    class Meta:
        unique_together = [("kingdom", "skill")]
        ordering = ["skill"]
        verbose_name_plural = "kingdom skill proficiencies"

    def __str__(self):
        return f"{self.get_skill_display()} ({self.get_proficiency_display()})"

    @property
    def key_ability(self):
        return SKILL_KEY_ABILITY.get(self.skill)

    @property
    def proficiency_bonus(self):
        bonus = PROFICIENCY_BONUS.get(self.proficiency, 0)
        if bonus == 0:
            return 0
        return self.kingdom.level + bonus


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

    class Meta:
        unique_together = [("user", "kingdom")]

    def __str__(self):
        return f"{self.user} - {self.kingdom} ({self.get_role_display()})"
