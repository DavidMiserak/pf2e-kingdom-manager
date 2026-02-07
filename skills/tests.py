from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kingdoms.constants import KingdomSkill, Proficiency
from kingdoms.models import Kingdom, KingdomMembership, MembershipRole

from .models import KingdomSkillProficiency

User = get_user_model()


class KingdomSkillProficiencyTests(TestCase):
    def setUp(self):
        self.kingdom = Kingdom.objects.create(name="Test Kingdom", level=5)
        self.skill = KingdomSkillProficiency.objects.create(
            kingdom=self.kingdom,
            skill=KingdomSkill.ARTS,
        )

    def test_str(self):
        self.assertEqual(str(self.skill), "Arts (Untrained)")

    def test_key_ability(self):
        self.assertEqual(self.skill.key_ability, "culture")

    def test_proficiency_bonus_untrained(self):
        self.assertEqual(self.skill.proficiency_bonus, 0)

    def test_proficiency_bonus_trained(self):
        self.skill.proficiency = Proficiency.TRAINED
        self.assertEqual(self.skill.proficiency_bonus, 7)  # 5 + 2

    def test_proficiency_bonus_expert(self):
        self.skill.proficiency = Proficiency.EXPERT
        self.assertEqual(self.skill.proficiency_bonus, 9)  # 5 + 4

    def test_proficiency_bonus_master(self):
        self.skill.proficiency = Proficiency.MASTER
        self.assertEqual(self.skill.proficiency_bonus, 11)  # 5 + 6

    def test_proficiency_bonus_legendary(self):
        self.skill.proficiency = Proficiency.LEGENDARY
        self.assertEqual(self.skill.proficiency_bonus, 13)  # 5 + 8


class SkillsUpdateViewTests(TestCase):
    def setUp(self):
        self.gm = User.objects.create_user(
            username="gm",
            email="gm@example.com",
            password="testpass123",  # nosec B106
        )
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")
        self.kingdom.initialize_defaults()
        KingdomMembership.objects.create(
            user=self.gm,
            kingdom=self.kingdom,
            role=MembershipRole.GM,
        )
        self.url = reverse("skills:skills_update", kwargs={"pk": self.kingdom.pk})

    def test_gm_can_access(self):
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kingdoms/skills_form.html")
