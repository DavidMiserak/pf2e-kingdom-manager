from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kingdoms.models import Kingdom, KingdomMembership, MembershipRole

from .models import LeadershipAssignment, LeadershipRole

User = get_user_model()


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
            password="testpass123",  # nosec B106
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
