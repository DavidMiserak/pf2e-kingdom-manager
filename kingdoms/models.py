import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


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


class ActivityTrait(models.TextChoices):
    UPKEEP = "upkeep", "Upkeep"
    COMMERCE = "commerce", "Commerce"
    LEADERSHIP = "leadership", "Leadership"
    REGION = "region", "Region"
    CIVIC = "civic", "Civic"
    FORTUNE = "fortune", "Fortune"
    DOWNTIME = "downtime", "Downtime"


class DegreeOfSuccess(models.TextChoices):
    CRITICAL_SUCCESS = "critical_success", "Critical Success"
    SUCCESS = "success", "Success"
    FAILURE = "failure", "Failure"
    CRITICAL_FAILURE = "critical_failure", "Critical Failure"


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
    government = models.CharField(
        max_length=11,
        choices=Government,
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
    character_name = models.CharField(max_length=100, default="Bilbo")

    class Meta:
        unique_together = [("user", "kingdom")]

    def __str__(self):
        return f"{self.user} - {self.kingdom} ({self.get_role_display()})"


class KingdomTurn(models.Model):
    kingdom = models.ForeignKey(
        Kingdom,
        on_delete=models.CASCADE,
        related_name="turns",
    )
    turn_number = models.PositiveSmallIntegerField()
    in_game_month = models.CharField(max_length=50, blank=True, default="")

    # Snapshot of starting state
    starting_rp = models.PositiveIntegerField(null=True, blank=True)
    resource_dice_rolled = models.CharField(max_length=50, blank=True, default="")

    # Commerce phase tracking
    collected_taxes = models.BooleanField(default=False)
    improved_lifestyle = models.BooleanField(default=False)
    tapped_treasury = models.BooleanField(default=False)

    # End-of-turn results
    ending_rp = models.PositiveIntegerField(null=True, blank=True)
    rp_converted_to_xp = models.PositiveIntegerField(null=True, blank=True)
    xp_gained = models.PositiveIntegerField(null=True, blank=True)
    leveled_up = models.BooleanField(default=False)

    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [("kingdom", "turn_number")]
        ordering = ["-turn_number"]

    def __str__(self):
        return f"Turn {self.turn_number}"

    @property
    def is_complete(self):
        return self.completed_at is not None

    @property
    def activity_count(self):
        return self.activities.count()

    def complete_turn(self):
        self.completed_at = timezone.now()
        self.save(update_fields=["completed_at"])


class ActivityLog(models.Model):
    kingdom = models.ForeignKey(
        Kingdom,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    turn = models.ForeignKey(
        KingdomTurn,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    activity_name = models.CharField(max_length=100)
    activity_trait = models.CharField(max_length=15, choices=ActivityTrait)
    skill_used = models.CharField(
        max_length=12,
        choices=KingdomSkill,
        blank=True,
        default="",
    )
    performed_by = models.ForeignKey(
        LeadershipAssignment,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="activities",
    )

    # Roll tracking (all optional)
    roll_result = models.PositiveSmallIntegerField(null=True, blank=True)
    total_modifier = models.SmallIntegerField(null=True, blank=True)
    dc = models.PositiveSmallIntegerField(null=True, blank=True)
    degree_of_success = models.CharField(
        max_length=16,
        choices=DegreeOfSuccess,
        blank=True,
        default="",
    )

    notes = models.TextField(blank=True, default="")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="activities_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "activity log"
        verbose_name_plural = "activity logs"

    def __str__(self):
        return self.activity_name

    @property
    def performer_name(self):
        if self.performed_by:
            return self.performed_by.display_name
        return "Kingdom"

    @property
    def total_result(self):
        if self.roll_result is not None and self.total_modifier is not None:
            return self.roll_result + self.total_modifier
        return None

    def calculate_degree_of_success(self):
        if self.roll_result is None or self.total_modifier is None or self.dc is None:
            return ""
        total = self.total_result
        # Start with standard determination
        if total >= self.dc + 10:
            degree = DegreeOfSuccess.CRITICAL_SUCCESS
        elif total >= self.dc:
            degree = DegreeOfSuccess.SUCCESS
        elif total <= self.dc - 10:
            degree = DegreeOfSuccess.CRITICAL_FAILURE
        else:
            degree = DegreeOfSuccess.FAILURE
        # Natural 20 upgrades by one step
        if self.roll_result == 20:
            if degree == DegreeOfSuccess.FAILURE:
                degree = DegreeOfSuccess.SUCCESS
            elif degree == DegreeOfSuccess.SUCCESS:
                degree = DegreeOfSuccess.CRITICAL_SUCCESS
            elif degree == DegreeOfSuccess.CRITICAL_FAILURE:
                degree = DegreeOfSuccess.FAILURE
        # Natural 1 downgrades by one step
        elif self.roll_result == 1:
            if degree == DegreeOfSuccess.SUCCESS:
                degree = DegreeOfSuccess.FAILURE
            elif degree == DegreeOfSuccess.FAILURE:
                degree = DegreeOfSuccess.CRITICAL_FAILURE
            elif degree == DegreeOfSuccess.CRITICAL_SUCCESS:
                degree = DegreeOfSuccess.SUCCESS
        return degree
