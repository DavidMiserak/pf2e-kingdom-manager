from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import (
    Kingdom,
    KingdomMembership,
    KingdomSkill,
    KingdomSkillProficiency,
    LeadershipAssignment,
    LeadershipRole,
    MembershipRole,
    Proficiency,
)

User = get_user_model()


class KingdomModelTests(TestCase):
    def setUp(self):
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")

    def test_str(self):
        self.assertEqual(str(self.kingdom), "Test Kingdom")

    def test_defaults(self):
        k = self.kingdom
        self.assertEqual(k.level, 1)
        self.assertEqual(k.xp, 0)
        self.assertEqual(k.culture_score, 10)
        self.assertEqual(k.economy_score, 10)
        self.assertEqual(k.loyalty_score, 10)
        self.assertEqual(k.stability_score, 10)
        self.assertEqual(k.unrest, 0)
        self.assertEqual(k.fame_points, 0)
        self.assertEqual(k.fame_type, "fame")
        self.assertEqual(k.resource_points, 0)

    def test_ability_modifier_standard(self):
        self.assertEqual(self.kingdom.culture_modifier, 0)  # score 10

    def test_ability_modifier_high(self):
        self.kingdom.culture_score = 14
        self.assertEqual(self.kingdom.culture_modifier, 2)

    def test_ability_modifier_low(self):
        self.kingdom.economy_score = 8
        self.assertEqual(self.kingdom.economy_modifier, -1)

    def test_ability_modifier_odd(self):
        self.kingdom.loyalty_score = 13
        self.assertEqual(self.kingdom.loyalty_modifier, 1)

    def test_get_ability_modifier(self):
        self.kingdom.stability_score = 16
        self.assertEqual(self.kingdom.get_ability_modifier("stability"), 3)

    def test_size_category_default(self):
        self.assertEqual(self.kingdom.size_category, "Territory")

    def test_commodity_storage_limit_default(self):
        self.assertEqual(self.kingdom.commodity_storage_limit, 4)

    def test_resource_die_type_default(self):
        self.assertEqual(self.kingdom.resource_die_type, "d4")

    def test_control_dc(self):
        # level 1, size modifier 0 → 14 + 1 + 0 = 15
        self.assertEqual(self.kingdom.control_dc, 15)

    def test_control_dc_higher_level(self):
        self.kingdom.level = 5
        self.assertEqual(self.kingdom.control_dc, 19)

    def test_unrest_penalty_zero(self):
        self.assertEqual(self.kingdom.unrest_penalty, 0)

    def test_unrest_penalty_low(self):
        self.kingdom.unrest = 1
        self.assertEqual(self.kingdom.unrest_penalty, -1)

    def test_unrest_penalty_medium(self):
        self.kingdom.unrest = 7
        self.assertEqual(self.kingdom.unrest_penalty, -2)

    def test_unrest_penalty_high(self):
        self.kingdom.unrest = 12
        self.assertEqual(self.kingdom.unrest_penalty, -3)

    def test_unrest_penalty_extreme(self):
        self.kingdom.unrest = 15
        self.assertEqual(self.kingdom.unrest_penalty, -4)

    def test_ruin_defaults(self):
        k = self.kingdom
        self.assertEqual(k.corruption_threshold, 10)
        self.assertEqual(k.corruption_points, 0)
        self.assertEqual(k.corruption_penalty, 0)
        self.assertEqual(k.crime_threshold, 10)
        self.assertEqual(k.decay_threshold, 10)
        self.assertEqual(k.strife_threshold, 10)

    def test_initialize_defaults(self):
        self.kingdom.initialize_defaults()
        self.assertEqual(self.kingdom.leadership_assignments.count(), 8)
        self.assertEqual(self.kingdom.skill_proficiencies.count(), 16)

    def test_initialize_defaults_idempotent(self):
        self.kingdom.initialize_defaults()
        self.kingdom.initialize_defaults()
        self.assertEqual(self.kingdom.leadership_assignments.count(), 8)
        self.assertEqual(self.kingdom.skill_proficiencies.count(), 16)


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


class KingdomMembershipTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",  # nosec B106
        )
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")
        self.membership = KingdomMembership.objects.create(
            user=self.user,
            kingdom=self.kingdom,
            role=MembershipRole.GM,
        )

    def test_str(self):
        self.assertIn("Test Kingdom", str(self.membership))
        self.assertIn("Game Master", str(self.membership))

    def test_unique_constraint(self):
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            KingdomMembership.objects.create(
                user=self.user,
                kingdom=self.kingdom,
                role=MembershipRole.PLAYER,
            )


class KingdomListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",  # nosec B106
        )
        self.kingdom = Kingdom.objects.create(name="My Kingdom")
        KingdomMembership.objects.create(
            user=self.user,
            kingdom=self.kingdom,
            role=MembershipRole.GM,
        )
        self.url = reverse("kingdoms:kingdom_list")

    def test_anonymous_redirect(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_shows_kingdoms(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Kingdom")

    def test_only_shows_member_kingdoms(self):
        other_kingdom = Kingdom.objects.create(name="Other Kingdom")
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertContains(response, "My Kingdom")
        self.assertNotContains(response, "Other Kingdom")


class KingdomCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",  # nosec B106
        )
        self.url = reverse("kingdoms:kingdom_create")

    def test_anonymous_redirect(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kingdoms/kingdom_form.html")

    def test_create_kingdom(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, {"name": "New Kingdom", "fame_type": "fame"}
        )
        kingdom = Kingdom.objects.get(name="New Kingdom")
        self.assertRedirects(
            response,
            reverse("kingdoms:kingdom_detail", kwargs={"pk": kingdom.pk}),
        )
        # Verify GM membership created
        self.assertTrue(
            KingdomMembership.objects.filter(
                user=self.user, kingdom=kingdom, role=MembershipRole.GM
            ).exists()
        )
        # Verify defaults initialized
        self.assertEqual(kingdom.leadership_assignments.count(), 8)
        self.assertEqual(kingdom.skill_proficiencies.count(), 16)


class KingdomDetailViewTests(TestCase):
    def setUp(self):
        self.gm = User.objects.create_user(
            username="gm",
            email="gm@example.com",
            password="testpass123",  # nosec B106
        )
        self.player = User.objects.create_user(
            username="player",
            email="player@example.com",
            password="testpass123",  # nosec B106
        )
        self.outsider = User.objects.create_user(
            username="outsider",
            email="outsider@example.com",
            password="testpass123",  # nosec B106
        )
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")
        self.kingdom.initialize_defaults()
        KingdomMembership.objects.create(
            user=self.gm,
            kingdom=self.kingdom,
            role=MembershipRole.GM,
        )
        KingdomMembership.objects.create(
            user=self.player,
            kingdom=self.kingdom,
            role=MembershipRole.PLAYER,
        )
        self.url = reverse("kingdoms:kingdom_detail", kwargs={"pk": self.kingdom.pk})

    def test_anonymous_redirect(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_gm_can_view(self):
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Kingdom")
        self.assertContains(response, "Edit Stats")

    def test_player_can_view(self):
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Kingdom")
        self.assertNotContains(response, "Edit Stats")

    def test_non_member_gets_404(self):
        self.client.force_login(self.outsider)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class KingdomUpdateViewTests(TestCase):
    def setUp(self):
        self.gm = User.objects.create_user(
            username="gm",
            email="gm@example.com",
            password="testpass123",  # nosec B106
        )
        self.player = User.objects.create_user(
            username="player",
            email="player@example.com",
            password="testpass123",  # nosec B106
        )
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")
        KingdomMembership.objects.create(
            user=self.gm,
            kingdom=self.kingdom,
            role=MembershipRole.GM,
        )
        KingdomMembership.objects.create(
            user=self.player,
            kingdom=self.kingdom,
            role=MembershipRole.PLAYER,
        )
        self.url = reverse("kingdoms:kingdom_update", kwargs={"pk": self.kingdom.pk})

    def test_player_gets_404(self):
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_gm_can_access(self):
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_gm_can_update(self):
        self.client.force_login(self.gm)
        data = {
            "name": "Updated Kingdom",
            "culture_score": 14,
            "economy_score": 12,
            "loyalty_score": 10,
            "stability_score": 10,
            "level": 3,
            "xp": 500,
            "unrest": 2,
            "fame_points": 1,
            "fame_type": "fame",
            "resource_points": 50,
            "bonus_dice": 1,
            "penalty_dice": 0,
            "corruption_points": 3,
            "corruption_threshold": 10,
            "corruption_penalty": 0,
            "crime_points": 0,
            "crime_threshold": 10,
            "crime_penalty": 0,
            "strife_points": 0,
            "strife_threshold": 10,
            "strife_penalty": 0,
            "decay_points": 0,
            "decay_threshold": 10,
            "decay_penalty": 0,
            "food": 2,
            "lumber": 3,
            "ore": 1,
            "stone": 0,
            "luxuries": 0,
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,
            reverse("kingdoms:kingdom_detail", kwargs={"pk": self.kingdom.pk}),
        )
        self.kingdom.refresh_from_db()
        self.assertEqual(self.kingdom.name, "Updated Kingdom")
        self.assertEqual(self.kingdom.culture_score, 14)
        self.assertEqual(self.kingdom.level, 3)


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
        self.url = reverse("kingdoms:leadership_update", kwargs={"pk": self.kingdom.pk})

    def test_gm_can_access(self):
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kingdoms/leadership_form.html")


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
        self.url = reverse("kingdoms:skills_update", kwargs={"pk": self.kingdom.pk})

    def test_gm_can_access(self):
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kingdoms/skills_form.html")


class MemberManageViewTests(TestCase):
    def setUp(self):
        self.gm = User.objects.create_user(
            username="gm",
            email="gm@example.com",
            password="testpass123",  # nosec B106
        )
        self.player = User.objects.create_user(
            username="player",
            email="player@example.com",
            password="testpass123",  # nosec B106
        )
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")
        KingdomMembership.objects.create(
            user=self.gm,
            kingdom=self.kingdom,
            role=MembershipRole.GM,
        )
        self.url = reverse("kingdoms:member_manage", kwargs={"pk": self.kingdom.pk})

    def test_gm_can_access(self):
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kingdoms/member_list.html")

    def test_player_gets_404(self):
        KingdomMembership.objects.create(
            user=self.player,
            kingdom=self.kingdom,
            role=MembershipRole.PLAYER,
        )
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_invite_url_in_context(self):
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertIn("invite_url", response.context)
        self.assertIn(str(self.kingdom.invite_code), response.context["invite_url"])

    def test_remove_member(self):
        membership = KingdomMembership.objects.create(
            user=self.player,
            kingdom=self.kingdom,
            role=MembershipRole.PLAYER,
        )
        self.client.force_login(self.gm)
        response = self.client.post(
            self.url,
            {"membership_id": membership.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(KingdomMembership.objects.filter(pk=membership.pk).exists())

    def test_cannot_remove_self(self):
        self.client.force_login(self.gm)
        gm_membership = KingdomMembership.objects.get(
            user=self.gm, kingdom=self.kingdom
        )
        response = self.client.post(
            self.url,
            {"membership_id": gm_membership.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(KingdomMembership.objects.filter(pk=gm_membership.pk).exists())


class JoinKingdomViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="newplayer",
            email="newplayer@example.com",
            password="testpass123",  # nosec B106
        )
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")
        self.kingdom.initialize_defaults()
        self.url = reverse(
            "kingdoms:join",
            kwargs={"invite_code": self.kingdom.invite_code},
        )

    def test_anonymous_redirect(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_join_kingdom(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse("kingdoms:kingdom_detail", kwargs={"pk": self.kingdom.pk}),
        )
        self.assertTrue(
            KingdomMembership.objects.filter(
                user=self.user,
                kingdom=self.kingdom,
                role=MembershipRole.PLAYER,
            ).exists()
        )

    def test_already_a_member(self):
        KingdomMembership.objects.create(
            user=self.user,
            kingdom=self.kingdom,
            role=MembershipRole.PLAYER,
        )
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse("kingdoms:kingdom_detail", kwargs={"pk": self.kingdom.pk}),
        )
        self.assertEqual(
            KingdomMembership.objects.filter(
                user=self.user, kingdom=self.kingdom
            ).count(),
            1,
        )

    def test_invalid_code_404(self):
        self.client.force_login(self.user)
        import uuid

        bad_url = reverse("kingdoms:join", kwargs={"invite_code": uuid.uuid4()})
        response = self.client.get(bad_url)
        self.assertEqual(response.status_code, 404)


class RegenerateInviteViewTests(TestCase):
    def setUp(self):
        self.gm = User.objects.create_user(
            username="gm",
            email="gm@example.com",
            password="testpass123",  # nosec B106
        )
        self.player = User.objects.create_user(
            username="player",
            email="player@example.com",
            password="testpass123",  # nosec B106
        )
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")
        KingdomMembership.objects.create(
            user=self.gm,
            kingdom=self.kingdom,
            role=MembershipRole.GM,
        )
        KingdomMembership.objects.create(
            user=self.player,
            kingdom=self.kingdom,
            role=MembershipRole.PLAYER,
        )
        self.url = reverse("kingdoms:regenerate_invite", kwargs={"pk": self.kingdom.pk})

    def test_gm_can_regenerate(self):
        old_code = self.kingdom.invite_code
        self.client.force_login(self.gm)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.kingdom.refresh_from_db()
        self.assertNotEqual(self.kingdom.invite_code, old_code)

    def test_player_cannot_regenerate(self):
        self.client.force_login(self.player)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)


class KingdomDeleteViewTests(TestCase):
    def setUp(self):
        self.gm = User.objects.create_user(
            username="gm",
            email="gm@example.com",
            password="testpass123",  # nosec B106
        )
        self.player = User.objects.create_user(
            username="player",
            email="player@example.com",
            password="testpass123",  # nosec B106
        )
        self.kingdom = Kingdom.objects.create(name="Doomed Kingdom")
        KingdomMembership.objects.create(
            user=self.gm,
            kingdom=self.kingdom,
            role=MembershipRole.GM,
        )
        KingdomMembership.objects.create(
            user=self.player,
            kingdom=self.kingdom,
            role=MembershipRole.PLAYER,
        )
        self.url = reverse("kingdoms:kingdom_delete", kwargs={"pk": self.kingdom.pk})

    def test_gm_sees_confirmation(self):
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Doomed Kingdom")
        self.assertTemplateUsed(response, "kingdoms/kingdom_confirm_delete.html")

    def test_gm_can_delete(self):
        self.client.force_login(self.gm)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("kingdoms:kingdom_list"))
        self.assertFalse(Kingdom.objects.filter(pk=self.kingdom.pk).exists())

    def test_player_cannot_delete(self):
        self.client.force_login(self.player)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Kingdom.objects.filter(pk=self.kingdom.pk).exists())

    def test_anonymous_redirect(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
