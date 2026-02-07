from django.db import models

from kingdoms.constants import (
    PROFICIENCY_BONUS,
    AbilityScore,
    KingdomSkill,
    Proficiency,
)

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


class KingdomSkillProficiency(models.Model):
    kingdom = models.ForeignKey(
        "kingdoms.Kingdom",
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
        db_table = "kingdoms_kingdomskillproficiency"

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
