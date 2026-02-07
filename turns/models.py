from django.conf import settings
from django.db import models
from django.utils import timezone

from kingdoms.constants import GolarionMonth, KingdomSkill, ResourceDie


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


class KingdomTurn(models.Model):
    kingdom = models.ForeignKey(
        "kingdoms.Kingdom",
        on_delete=models.CASCADE,
        related_name="turns",
    )
    turn_number = models.PositiveSmallIntegerField()
    in_game_month = models.CharField(
        max_length=50,
        choices=GolarionMonth,
        blank=True,
        default="",
    )

    # Snapshot of starting state
    starting_rp = models.PositiveIntegerField(null=True, blank=True)
    resource_dice_rolled = models.CharField(
        max_length=50,
        choices=ResourceDie,
        blank=True,
        default="",
    )

    # Commerce phase tracking
    collected_taxes = models.BooleanField(default=False)
    improved_lifestyle = models.BooleanField(default=False)
    tapped_treasury = models.BooleanField(default=False)

    # Event phase tracking
    event_occurred = models.BooleanField(default=False)
    event_xp = models.PositiveIntegerField(default=0)

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
        indexes = [
            models.Index(fields=["kingdom", "-turn_number"]),
            models.Index(fields=["kingdom", "completed_at"]),
        ]
        db_table = "kingdoms_kingdomturn"

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
        "kingdoms.Kingdom",
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
        "leadership.LeadershipAssignment",
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
        indexes = [
            models.Index(fields=["turn", "-created_at"]),
        ]
        db_table = "kingdoms_activitylog"

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
