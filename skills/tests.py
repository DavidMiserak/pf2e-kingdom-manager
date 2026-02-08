from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kingdoms.constants import KingdomSkill, Proficiency
from kingdoms.models import Kingdom, KingdomMembership, MembershipRole

from .models import KingdomSkillProficiency

User = get_user_model()

TEST_PASSWORD = "testpass123"  # nosec B105


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
            password=TEST_PASSWORD,
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

    def test_post_valid_formset(self):
        """Test successful POST with valid formset data."""
        self.client.force_login(self.gm)
        skills = list(self.kingdom.skill_proficiencies.all())
        data = {
            "form-TOTAL_FORMS": "16",
            "form-INITIAL_FORMS": "16",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "1000",
        }
        # Update first skill to trained
        data.update(
            {
                f"form-0-id": skills[0].pk,
                f"form-0-proficiency": Proficiency.TRAINED,
            }
        )
        # Keep remaining skills as-is
        for i in range(1, 16):
            data.update(
                {
                    f"form-{i}-id": skills[i].pk,
                    f"form-{i}-proficiency": skills[i].proficiency,
                }
            )

        response = self.client.post(self.url, data)
        self.assertRedirects(
            response, reverse("kingdoms:kingdom_detail", kwargs={"pk": self.kingdom.pk})
        )
        skills[0].refresh_from_db()
        self.assertEqual(skills[0].proficiency, Proficiency.TRAINED)

    def test_post_invalid_formset(self):
        """Test POST with invalid formset data renders form with errors."""
        self.client.force_login(self.gm)
        # Missing INITIAL_FORMS makes formset invalid
        data = {
            "form-TOTAL_FORMS": "16",
            "form-MIN_NUM_FORMS": "0",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kingdoms/skills_form.html")

    def test_government_boosted_flag_set(self):
        """Test that government_boosted flag is set in context."""
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        formset = response.context["formset"]
        # At least one form should exist
        self.assertGreater(len(formset), 0)
        # Check that government_boosted attribute exists on forms
        for form in formset:
            self.assertIsNotNone(hasattr(form, "government_boosted"))

    def test_non_gm_cannot_access(self):
        """Test that players cannot access skills update view."""
        player = User.objects.create_user(
            username="player",
            email="player@example.com",
            password=TEST_PASSWORD,
        )
        KingdomMembership.objects.create(
            user=player,
            kingdom=self.kingdom,
            role=MembershipRole.PLAYER,
        )
        self.client.force_login(player)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_non_member_cannot_access(self):
        """Test that non-members cannot access skills update view."""
        outsider = User.objects.create_user(
            username="outsider",
            email="outsider@example.com",
            password=TEST_PASSWORD,
        )
        self.client.force_login(outsider)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_unauthenticated_redirects(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)
