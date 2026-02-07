"""Shared enums and constants used across multiple apps.

These are pure enum/dict definitions with no model dependencies,
extracted to avoid circular imports between apps.
"""

from django.db import models


class GolarionMonth(models.TextChoices):
    ABADIUS = "abadius", "Abadius"
    CALISTRIL = "calistril", "Calistril"
    PHARAST = "pharast", "Pharast"
    GOZRAN = "gozran", "Gozran"
    DESNUS = "desnus", "Desnus"
    SARENITH = "sarenith", "Sarenith"
    ERASTUS = "erastus", "Erastus"
    ARODUS = "arodus", "Arodus"
    ROVA = "rova", "Rova"
    LAMASHAN = "lamashan", "Lamashan"
    NETH = "neth", "Neth"
    KUTHONA = "kuthona", "Kuthona"


class ResourceDie(models.TextChoices):
    D4 = "d4", "d4"
    D6 = "d6", "d6"
    D8 = "d8", "d8"
    D10 = "d10", "d10"
    D12 = "d12", "d12"


class AbilityScore(models.TextChoices):
    CULTURE = "culture", "Culture"
    ECONOMY = "economy", "Economy"
    LOYALTY = "loyalty", "Loyalty"
    STABILITY = "stability", "Stability"


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
