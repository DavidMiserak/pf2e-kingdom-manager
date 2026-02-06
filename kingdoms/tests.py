from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import (
    ActivityLog,
    ActivityTrait,
    DegreeOfSuccess,
    Kingdom,
    KingdomMembership,
    KingdomSkill,
    KingdomSkillProficiency,
    KingdomTurn,
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
        self.assertContains(response, "fa-pen")  # Edit button icon

    def test_player_can_view(self):
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Kingdom")
        self.assertNotContains(response, "btn-outline-danger")  # No delete button

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

    def test_anonymous_redirect_delete(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class UpdateCharacterNameViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
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
        self.membership = KingdomMembership.objects.create(
            user=self.user,
            kingdom=self.kingdom,
            role=MembershipRole.PLAYER,
        )
        self.url = reverse(
            "kingdoms:update_character_name",
            kwargs={"pk": self.kingdom.pk},
        )

    def test_member_can_update_name(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {"character_name": "Gandalf"})
        self.assertRedirects(
            response,
            reverse("kingdoms:kingdom_detail", kwargs={"pk": self.kingdom.pk}),
        )
        self.membership.refresh_from_db()
        self.assertEqual(self.membership.character_name, "Gandalf")

    def test_default_character_name(self):
        self.assertEqual(self.membership.character_name, "Bilbo")

    def test_non_member_gets_404(self):
        self.client.force_login(self.outsider)
        response = self.client.post(self.url, {"character_name": "Sauron"})
        self.assertEqual(response.status_code, 404)


# --- Phase 2: Turn and Activity Tests ---


class KingdomTurnModelTests(TestCase):
    def setUp(self):
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")
        self.turn = KingdomTurn.objects.create(kingdom=self.kingdom, turn_number=1)

    def test_str(self):
        self.assertEqual(str(self.turn), "Turn 1")

    def test_is_complete_false(self):
        self.assertFalse(self.turn.is_complete)

    def test_complete_turn(self):
        self.turn.complete_turn()
        self.turn.refresh_from_db()
        self.assertTrue(self.turn.is_complete)
        self.assertIsNotNone(self.turn.completed_at)

    def test_activity_count_zero(self):
        self.assertEqual(self.turn.activity_count, 0)

    def test_activity_count_with_activities(self):
        ActivityLog.objects.create(
            kingdom=self.kingdom,
            turn=self.turn,
            activity_name="Claim Hex",
            activity_trait=ActivityTrait.REGION,
        )
        self.assertEqual(self.turn.activity_count, 1)

    def test_unique_together(self):
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            KingdomTurn.objects.create(kingdom=self.kingdom, turn_number=1)

    def test_ordering(self):
        turn2 = KingdomTurn.objects.create(kingdom=self.kingdom, turn_number=2)
        turns = list(self.kingdom.turns.all())
        self.assertEqual(turns[0], turn2)
        self.assertEqual(turns[1], self.turn)

    def test_cascade_delete(self):
        ActivityLog.objects.create(
            kingdom=self.kingdom,
            turn=self.turn,
            activity_name="Claim Hex",
            activity_trait=ActivityTrait.REGION,
        )
        self.turn.delete()
        self.assertEqual(ActivityLog.objects.count(), 0)


class ActivityLogModelTests(TestCase):
    def setUp(self):
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")
        self.kingdom.initialize_defaults()
        self.turn = KingdomTurn.objects.create(kingdom=self.kingdom, turn_number=1)
        self.ruler = self.kingdom.leadership_assignments.get(role=LeadershipRole.RULER)
        self.ruler.character_name = "King Arthur"
        self.ruler.is_vacant = False
        self.ruler.save()

    def test_str(self):
        activity = ActivityLog.objects.create(
            kingdom=self.kingdom,
            turn=self.turn,
            activity_name="Collect Taxes",
            activity_trait=ActivityTrait.COMMERCE,
        )
        self.assertEqual(str(activity), "Collect Taxes")

    def test_performer_name_with_performer(self):
        activity = ActivityLog.objects.create(
            kingdom=self.kingdom,
            turn=self.turn,
            activity_name="Quell Unrest",
            activity_trait=ActivityTrait.LEADERSHIP,
            performed_by=self.ruler,
        )
        self.assertEqual(activity.performer_name, "King Arthur")

    def test_performer_name_without_performer(self):
        activity = ActivityLog.objects.create(
            kingdom=self.kingdom,
            turn=self.turn,
            activity_name="Upkeep",
            activity_trait=ActivityTrait.UPKEEP,
        )
        self.assertEqual(activity.performer_name, "Kingdom")

    def test_total_result(self):
        activity = ActivityLog(roll_result=15, total_modifier=7)
        self.assertEqual(activity.total_result, 22)

    def test_total_result_none(self):
        activity = ActivityLog(roll_result=15)
        self.assertIsNone(activity.total_result)

    def test_calculate_degree_critical_success(self):
        activity = ActivityLog(roll_result=10, total_modifier=20, dc=20)
        self.assertEqual(
            activity.calculate_degree_of_success(),
            DegreeOfSuccess.CRITICAL_SUCCESS,
        )

    def test_calculate_degree_success(self):
        activity = ActivityLog(roll_result=10, total_modifier=10, dc=20)
        self.assertEqual(
            activity.calculate_degree_of_success(),
            DegreeOfSuccess.SUCCESS,
        )

    def test_calculate_degree_failure(self):
        activity = ActivityLog(roll_result=10, total_modifier=5, dc=20)
        self.assertEqual(
            activity.calculate_degree_of_success(),
            DegreeOfSuccess.FAILURE,
        )

    def test_calculate_degree_critical_failure(self):
        activity = ActivityLog(roll_result=5, total_modifier=0, dc=20)
        self.assertEqual(
            activity.calculate_degree_of_success(),
            DegreeOfSuccess.CRITICAL_FAILURE,
        )

    def test_calculate_degree_nat20_upgrades(self):
        # Nat 20, total 25 vs DC 26 = would be failure, upgrades to success
        activity = ActivityLog(roll_result=20, total_modifier=5, dc=26)
        self.assertEqual(
            activity.calculate_degree_of_success(),
            DegreeOfSuccess.SUCCESS,
        )

    def test_calculate_degree_nat20_success_to_crit(self):
        # Nat 20, total 27 vs DC 26 = success, upgrades to critical success
        activity = ActivityLog(roll_result=20, total_modifier=7, dc=26)
        self.assertEqual(
            activity.calculate_degree_of_success(),
            DegreeOfSuccess.CRITICAL_SUCCESS,
        )

    def test_calculate_degree_nat20_crit_failure_to_failure(self):
        # Nat 20, total 5 vs DC 20 = would be critical failure, upgrades to failure
        activity = ActivityLog(roll_result=20, total_modifier=-15, dc=20)
        self.assertEqual(
            activity.calculate_degree_of_success(),
            DegreeOfSuccess.FAILURE,
        )

    def test_calculate_degree_nat1_downgrades(self):
        # Nat 1, total 11 vs DC 10 = would be success, downgrades to failure
        activity = ActivityLog(roll_result=1, total_modifier=10, dc=10)
        self.assertEqual(
            activity.calculate_degree_of_success(),
            DegreeOfSuccess.FAILURE,
        )

    def test_calculate_degree_nat1_failure_to_crit(self):
        # Nat 1, total 8 vs DC 10 = failure, downgrades to critical failure
        activity = ActivityLog(roll_result=1, total_modifier=7, dc=10)
        self.assertEqual(
            activity.calculate_degree_of_success(),
            DegreeOfSuccess.CRITICAL_FAILURE,
        )

    def test_calculate_degree_nat1_crit_success_to_success(self):
        # Nat 1, total 35 vs DC 20 = would be critical success, downgrades to success
        activity = ActivityLog(roll_result=1, total_modifier=34, dc=20)
        self.assertEqual(
            activity.calculate_degree_of_success(),
            DegreeOfSuccess.SUCCESS,
        )

    def test_calculate_degree_missing_data(self):
        activity = ActivityLog(roll_result=10)
        self.assertEqual(activity.calculate_degree_of_success(), "")

    def test_performed_by_set_null(self):
        activity = ActivityLog.objects.create(
            kingdom=self.kingdom,
            turn=self.turn,
            activity_name="Lead Army",
            activity_trait=ActivityTrait.LEADERSHIP,
            performed_by=self.ruler,
        )
        self.ruler.delete()
        activity.refresh_from_db()
        self.assertIsNone(activity.performed_by)


class TurnCreateViewTests(TestCase):
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
        self.url = reverse("kingdoms:turn_create", kwargs={"pk": self.kingdom.pk})

    def test_gm_can_access(self):
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kingdoms/turn_form.html")

    def test_player_gets_404(self):
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_create_first_turn(self):
        self.client.force_login(self.gm)
        response = self.client.post(self.url, {"in_game_month": "Pharast"})
        turn = KingdomTurn.objects.get(kingdom=self.kingdom)
        self.assertEqual(turn.turn_number, 1)
        self.assertEqual(turn.in_game_month, "Pharast")
        self.assertRedirects(
            response,
            reverse(
                "kingdoms:turn_detail",
                kwargs={"pk": self.kingdom.pk, "turn_pk": turn.pk},
            ),
        )

    def test_auto_increment_turn_number(self):
        KingdomTurn.objects.create(kingdom=self.kingdom, turn_number=1)
        self.client.force_login(self.gm)
        self.client.post(self.url, {"in_game_month": "Gozran"})
        self.assertEqual(self.kingdom.turns.count(), 2)
        latest = self.kingdom.turns.first()
        self.assertEqual(latest.turn_number, 2)


class TurnDetailViewTests(TestCase):
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
        self.turn = KingdomTurn.objects.create(
            kingdom=self.kingdom, turn_number=1, in_game_month="Pharast"
        )
        self.url = reverse(
            "kingdoms:turn_detail",
            kwargs={"pk": self.kingdom.pk, "turn_pk": self.turn.pk},
        )

    def test_member_can_view(self):
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Turn 1")
        self.assertContains(response, "Pharast")

    def test_outsider_gets_404(self):
        self.client.force_login(self.outsider)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_activities_in_context(self):
        ActivityLog.objects.create(
            kingdom=self.kingdom,
            turn=self.turn,
            activity_name="Claim Hex",
            activity_trait=ActivityTrait.REGION,
        )
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertContains(response, "Claim Hex")

    def test_gm_sees_controls(self):
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertContains(response, "Complete Turn")
        self.assertContains(response, "Log Activity")

    def test_player_sees_log_button(self):
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertContains(response, "Log Activity")
        self.assertNotContains(response, "Complete Turn")


class TurnUpdateViewTests(TestCase):
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
        self.turn = KingdomTurn.objects.create(kingdom=self.kingdom, turn_number=1)
        self.url = reverse(
            "kingdoms:turn_update",
            kwargs={"pk": self.kingdom.pk, "turn_pk": self.turn.pk},
        )

    def test_gm_can_update(self):
        self.client.force_login(self.gm)
        response = self.client.post(
            self.url,
            {
                "in_game_month": "Gozran",
                "starting_rp": 50,
                "collected_taxes": True,
                "xp_gained": 20,
            },
        )
        self.turn.refresh_from_db()
        self.assertEqual(self.turn.in_game_month, "Gozran")
        self.assertEqual(self.turn.starting_rp, 50)
        self.assertTrue(self.turn.collected_taxes)
        self.assertEqual(self.turn.xp_gained, 20)

    def test_player_gets_404(self):
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class TurnDeleteViewTests(TestCase):
    def setUp(self):
        self.gm = User.objects.create_user(
            username="gm",
            email="gm@example.com",
            password="testpass123",  # nosec B106
        )
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")
        KingdomMembership.objects.create(
            user=self.gm,
            kingdom=self.kingdom,
            role=MembershipRole.GM,
        )
        self.turn = KingdomTurn.objects.create(kingdom=self.kingdom, turn_number=1)
        self.url = reverse(
            "kingdoms:turn_delete",
            kwargs={"pk": self.kingdom.pk, "turn_pk": self.turn.pk},
        )

    def test_gm_sees_confirmation(self):
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm Deletion")

    def test_gm_can_delete(self):
        self.client.force_login(self.gm)
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse("kingdoms:kingdom_detail", kwargs={"pk": self.kingdom.pk}),
        )
        self.assertFalse(KingdomTurn.objects.filter(pk=self.turn.pk).exists())

    def test_cascade_deletes_activities(self):
        ActivityLog.objects.create(
            kingdom=self.kingdom,
            turn=self.turn,
            activity_name="Test",
            activity_trait=ActivityTrait.LEADERSHIP,
        )
        self.client.force_login(self.gm)
        self.client.post(self.url)
        self.assertEqual(ActivityLog.objects.count(), 0)


class TurnCompleteViewTests(TestCase):
    def setUp(self):
        self.gm = User.objects.create_user(
            username="gm",
            email="gm@example.com",
            password="testpass123",  # nosec B106
        )
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")
        KingdomMembership.objects.create(
            user=self.gm,
            kingdom=self.kingdom,
            role=MembershipRole.GM,
        )
        self.turn = KingdomTurn.objects.create(kingdom=self.kingdom, turn_number=1)
        self.url = reverse(
            "kingdoms:turn_complete",
            kwargs={"pk": self.kingdom.pk, "turn_pk": self.turn.pk},
        )

    def test_gm_can_complete(self):
        self.client.force_login(self.gm)
        response = self.client.post(self.url)
        self.turn.refresh_from_db()
        self.assertTrue(self.turn.is_complete)

    def test_already_complete(self):
        self.turn.complete_turn()
        self.client.force_login(self.gm)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)


class ActivityCreateViewTests(TestCase):
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
        self.turn = KingdomTurn.objects.create(kingdom=self.kingdom, turn_number=1)
        self.url = reverse(
            "kingdoms:activity_create",
            kwargs={"pk": self.kingdom.pk, "turn_pk": self.turn.pk},
        )

    def test_gm_can_access(self):
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kingdoms/activity_form.html")

    def test_player_can_access(self):
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_outsider_gets_404(self):
        self.client.force_login(self.outsider)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_create_activity(self):
        self.client.force_login(self.gm)
        response = self.client.post(
            self.url,
            {
                "activity_name": "Collect Taxes",
                "activity_trait": ActivityTrait.COMMERCE,
            },
        )
        activity = ActivityLog.objects.get(kingdom=self.kingdom)
        self.assertEqual(activity.activity_name, "Collect Taxes")
        self.assertEqual(activity.turn, self.turn)
        self.assertEqual(activity.created_by, self.gm)

    def test_auto_calculate_degree(self):
        self.client.force_login(self.gm)
        self.client.post(
            self.url,
            {
                "activity_name": "Claim Hex",
                "activity_trait": ActivityTrait.REGION,
                "roll_result": 15,
                "total_modifier": 10,
                "dc": 20,
            },
        )
        activity = ActivityLog.objects.get(kingdom=self.kingdom)
        self.assertEqual(activity.degree_of_success, DegreeOfSuccess.SUCCESS)

    def test_manual_degree_not_overwritten(self):
        self.client.force_login(self.gm)
        self.client.post(
            self.url,
            {
                "activity_name": "Claim Hex",
                "activity_trait": ActivityTrait.REGION,
                "roll_result": 15,
                "total_modifier": 10,
                "dc": 20,
                "degree_of_success": DegreeOfSuccess.CRITICAL_SUCCESS,
            },
        )
        activity = ActivityLog.objects.get(kingdom=self.kingdom)
        self.assertEqual(activity.degree_of_success, DegreeOfSuccess.CRITICAL_SUCCESS)

    def test_player_cannot_add_to_completed_turn(self):
        self.turn.complete_turn()
        self.client.force_login(self.player)
        response = self.client.post(
            self.url,
            {
                "activity_name": "Collect Taxes",
                "activity_trait": ActivityTrait.COMMERCE,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ActivityLog.objects.count(), 0)

    def test_gm_can_add_to_completed_turn(self):
        self.turn.complete_turn()
        self.client.force_login(self.gm)
        self.client.post(
            self.url,
            {
                "activity_name": "Late Entry",
                "activity_trait": ActivityTrait.LEADERSHIP,
            },
        )
        self.assertEqual(ActivityLog.objects.count(), 1)


class ActivityUpdateViewTests(TestCase):
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
        self.other_player = User.objects.create_user(
            username="other",
            email="other@example.com",
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
        KingdomMembership.objects.create(
            user=self.other_player,
            kingdom=self.kingdom,
            role=MembershipRole.PLAYER,
        )
        self.turn = KingdomTurn.objects.create(kingdom=self.kingdom, turn_number=1)
        self.activity = ActivityLog.objects.create(
            kingdom=self.kingdom,
            turn=self.turn,
            activity_name="Collect Taxes",
            activity_trait=ActivityTrait.COMMERCE,
            created_by=self.player,
        )
        self.url = reverse(
            "kingdoms:activity_update",
            kwargs={
                "pk": self.kingdom.pk,
                "activity_pk": self.activity.pk,
            },
        )

    def test_creator_can_edit(self):
        self.client.force_login(self.player)
        response = self.client.post(
            self.url,
            {
                "activity_name": "Updated Activity",
                "activity_trait": ActivityTrait.COMMERCE,
            },
        )
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.activity_name, "Updated Activity")

    def test_gm_can_edit(self):
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_other_player_gets_404(self):
        self.client.force_login(self.other_player)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class ActivityDeleteViewTests(TestCase):
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
        self.other_player = User.objects.create_user(
            username="other",
            email="other@example.com",
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
        KingdomMembership.objects.create(
            user=self.other_player,
            kingdom=self.kingdom,
            role=MembershipRole.PLAYER,
        )
        self.turn = KingdomTurn.objects.create(kingdom=self.kingdom, turn_number=1)
        self.activity = ActivityLog.objects.create(
            kingdom=self.kingdom,
            turn=self.turn,
            activity_name="Collect Taxes",
            activity_trait=ActivityTrait.COMMERCE,
            created_by=self.player,
        )
        self.url = reverse(
            "kingdoms:activity_delete",
            kwargs={
                "pk": self.kingdom.pk,
                "activity_pk": self.activity.pk,
            },
        )

    def test_creator_can_delete(self):
        self.client.force_login(self.player)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ActivityLog.objects.filter(pk=self.activity.pk).exists())

    def test_gm_can_delete(self):
        self.client.force_login(self.gm)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ActivityLog.objects.filter(pk=self.activity.pk).exists())

    def test_other_player_gets_404(self):
        self.client.force_login(self.other_player)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(ActivityLog.objects.filter(pk=self.activity.pk).exists())
