from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kingdoms.models import Kingdom, KingdomMembership, MembershipRole

from .models import LeadershipAssignment, LeadershipRole

User = get_user_model()

TEST_PASSWORD = "testpass123"  # nosec B105


class LeadershipAssignmentTests(TestCase):
    def setUp(self):
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")
        self.assignment = LeadershipAssignment.objects.create(
            kingdom=self.kingdom,
            role=LeadershipRole.RULER,
        )

    def test_str_vacant(self):
        self.assertEqual(str(self.assignment), "Ruler - Vacant")

    def test_str_assigned(self):
        self.assignment.character_name = "King Arthur"
        self.assertEqual(str(self.assignment), "Ruler - King Arthur")

    def test_key_ability(self):
        self.assertEqual(self.assignment.key_ability, "loyalty")

    def test_status_bonus_not_invested(self):
        self.assertEqual(self.assignment.status_bonus, 0)

    def test_status_bonus_invested_low_level(self):
        self.assignment.is_invested = True
        self.assignment.is_vacant = False
        self.assertEqual(self.assignment.status_bonus, 1)

    def test_status_bonus_invested_mid_level(self):
        self.kingdom.level = 10
        self.kingdom.save()
        self.assignment.is_invested = True
        self.assignment.is_vacant = False
        self.assertEqual(self.assignment.status_bonus, 2)

    def test_status_bonus_invested_high_level(self):
        self.kingdom.level = 18
        self.kingdom.save()
        self.assignment.is_invested = True
        self.assignment.is_vacant = False
        self.assertEqual(self.assignment.status_bonus, 3)

    def test_status_bonus_invested_but_vacant(self):
        self.assignment.is_invested = True
        self.assignment.is_vacant = True
        self.assertEqual(self.assignment.status_bonus, 0)


class LeadershipUpdateViewTests(TestCase):
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
        self.url = reverse(
            "leadership:leadership_update", kwargs={"pk": self.kingdom.pk}
        )

    def test_gm_can_access(self):
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kingdoms/leadership_form.html")

    def test_post_valid_formset(self):
        """Test successful POST with valid formset data."""
        self.client.force_login(self.gm)
        # Get assignments in the same order as the formset will use
        assignments = list(self.kingdom.leadership_assignments.all())
        ruler = self.kingdom.leadership_assignments.get(role=LeadershipRole.RULER)

        data = {
            "form-TOTAL_FORMS": "8",
            "form-INITIAL_FORMS": "8",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "8",
        }

        # Build form data for all assignments in order
        for i, assignment in enumerate(assignments):
            is_ruler = assignment.role == LeadershipRole.RULER
            data.update(
                {
                    f"form-{i}-id": assignment.pk,
                    f"form-{i}-character_name": "King Arthur" if is_ruler else "",
                    f"form-{i}-is_pc": "on" if is_ruler else "",
                    f"form-{i}-is_invested": "on" if is_ruler else "",
                    f"form-{i}-is_vacant": "" if is_ruler else "on",
                    f"form-{i}-downtime_fulfilled": "on" if is_ruler else "",
                    f"form-{i}-user": "",
                }
            )

        response = self.client.post(self.url, data)
        self.assertRedirects(
            response, reverse("kingdoms:kingdom_detail", kwargs={"pk": self.kingdom.pk})
        )
        ruler.refresh_from_db()
        self.assertEqual(ruler.character_name, "King Arthur")
        self.assertTrue(ruler.is_pc)
        self.assertTrue(ruler.is_invested)
        self.assertFalse(ruler.is_vacant)

    def test_post_invalid_formset(self):
        """Test POST with invalid formset data renders form with errors."""
        self.client.force_login(self.gm)
        # Missing management form data makes formset invalid
        data = {
            "form-TOTAL_FORMS": "1",
            "form-INITIAL_FORMS": "8",  # Mismatch causes validation error
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kingdoms/leadership_form.html")

    def test_non_gm_cannot_access(self):
        """Test that players cannot access leadership update view."""
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
        """Test that non-members cannot access leadership update view."""
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
