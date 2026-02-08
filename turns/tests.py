from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from kingdoms.models import Kingdom, KingdomMembership, MembershipRole
from leadership.models import LeadershipRole

from .models import ActivityLog, ActivityTrait, DegreeOfSuccess, KingdomTurn

User = get_user_model()

TEST_PASSWORD = "testpass123"  # nosec B106


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
            password=TEST_PASSWORD,
        )
        self.player = User.objects.create_user(
            username="player",
            email="player@example.com",
            password=TEST_PASSWORD,
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
        self.url = reverse("turns:turn_create", kwargs={"pk": self.kingdom.pk})

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
        response = self.client.post(self.url, {"in_game_month": "pharast"})
        turn = KingdomTurn.objects.get(kingdom=self.kingdom)
        self.assertEqual(turn.turn_number, 1)
        self.assertEqual(turn.in_game_month, "pharast")
        self.assertRedirects(
            response,
            reverse(
                "turns:turn_detail",
                kwargs={"pk": self.kingdom.pk, "turn_pk": turn.pk},
            ),
        )

    def test_auto_increment_turn_number(self):
        KingdomTurn.objects.create(kingdom=self.kingdom, turn_number=1)
        self.client.force_login(self.gm)
        self.client.post(self.url, {"in_game_month": "gozran"})
        self.assertEqual(self.kingdom.turns.count(), 2)
        latest = self.kingdom.turns.first()
        self.assertEqual(latest.turn_number, 2)


class TurnDetailViewTests(TestCase):
    def setUp(self):
        self.gm = User.objects.create_user(
            username="gm",
            email="gm@example.com",
            password=TEST_PASSWORD,
        )
        self.player = User.objects.create_user(
            username="player",
            email="player@example.com",
            password=TEST_PASSWORD,
        )
        self.outsider = User.objects.create_user(
            username="outsider",
            email="outsider@example.com",
            password=TEST_PASSWORD,
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
            "turns:turn_detail",
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

    def test_event_phase_displays_when_event_occurred(self):
        self.turn.event_occurred = True
        self.turn.event_xp = 30
        self.turn.save()

        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertContains(response, "Event Phase")
        self.assertContains(response, "Random Event Occurred")
        self.assertContains(response, "Event XP: 30")

    def test_event_phase_hidden_when_no_event(self):
        # Turn with event_occurred=False and event_xp=0 shouldn't show Event Phase
        self.client.force_login(self.gm)
        response = self.client.get(self.url)
        self.assertNotContains(response, "Event Phase")


class TurnUpdateViewTests(TestCase):
    def setUp(self):
        self.gm = User.objects.create_user(
            username="gm",
            email="gm@example.com",
            password=TEST_PASSWORD,
        )
        self.player = User.objects.create_user(
            username="player",
            email="player@example.com",
            password=TEST_PASSWORD,
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
            "turns:turn_update",
            kwargs={"pk": self.kingdom.pk, "turn_pk": self.turn.pk},
        )

    def test_gm_can_update(self):
        self.client.force_login(self.gm)
        response = self.client.post(
            self.url,
            {
                "in_game_month": "gozran",
                "starting_rp": 50,
                "resource_dice_rolled": "",
                "collected_taxes": True,
                "improved_lifestyle": False,
                "tapped_treasury": False,
                "event_occurred": False,
                "event_xp": 0,
                "xp_gained": 20,
                "leveled_up": False,
                "notes": "",
            },
        )
        self.turn.refresh_from_db()
        self.assertEqual(self.turn.in_game_month, "gozran")
        self.assertEqual(self.turn.starting_rp, 50)
        self.assertTrue(self.turn.collected_taxes)
        self.assertEqual(self.turn.xp_gained, 20)

    def test_gm_can_set_event_occurred(self):
        self.client.force_login(self.gm)
        response = self.client.post(
            self.url,
            {
                "in_game_month": "gozran",
                "starting_rp": 50,
                "resource_dice_rolled": "",
                "collected_taxes": False,
                "improved_lifestyle": False,
                "tapped_treasury": False,
                "event_occurred": True,
                "event_xp": 30,
                "xp_gained": 50,
                "leveled_up": False,
                "notes": "Random event occurred",
            },
        )
        self.turn.refresh_from_db()
        self.assertTrue(self.turn.event_occurred)
        self.assertEqual(self.turn.event_xp, 30)
        self.assertEqual(self.turn.xp_gained, 50)

    def test_gm_can_clear_event(self):
        # Verify event fields can be cleared/set to defaults
        self.turn.event_occurred = True
        self.turn.event_xp = 30
        self.turn.save()

        self.client.force_login(self.gm)
        response = self.client.post(
            self.url,
            {
                "in_game_month": "gozran",
                "starting_rp": 50,
                "resource_dice_rolled": "",
                "collected_taxes": False,
                "improved_lifestyle": False,
                "tapped_treasury": False,
                "event_occurred": False,
                "event_xp": 0,
                "xp_gained": 0,
                "leveled_up": False,
                "notes": "",
            },
        )
        self.turn.refresh_from_db()
        self.assertFalse(self.turn.event_occurred)
        self.assertEqual(self.turn.event_xp, 0)

    def test_player_gets_404(self):
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class TurnDeleteViewTests(TestCase):
    def setUp(self):
        self.gm = User.objects.create_user(
            username="gm",
            email="gm@example.com",
            password=TEST_PASSWORD,
        )
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")
        KingdomMembership.objects.create(
            user=self.gm,
            kingdom=self.kingdom,
            role=MembershipRole.GM,
        )
        self.turn = KingdomTurn.objects.create(kingdom=self.kingdom, turn_number=1)
        self.url = reverse(
            "turns:turn_delete",
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
            password=TEST_PASSWORD,
        )
        self.kingdom = Kingdom.objects.create(name="Test Kingdom")
        KingdomMembership.objects.create(
            user=self.gm,
            kingdom=self.kingdom,
            role=MembershipRole.GM,
        )
        self.turn = KingdomTurn.objects.create(kingdom=self.kingdom, turn_number=1)
        self.url = reverse(
            "turns:turn_complete",
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
            password=TEST_PASSWORD,
        )
        self.player = User.objects.create_user(
            username="player",
            email="player@example.com",
            password=TEST_PASSWORD,
        )
        self.outsider = User.objects.create_user(
            username="outsider",
            email="outsider@example.com",
            password=TEST_PASSWORD,
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
            "turns:activity_create",
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
            password=TEST_PASSWORD,
        )
        self.player = User.objects.create_user(
            username="player",
            email="player@example.com",
            password=TEST_PASSWORD,
        )
        self.other_player = User.objects.create_user(
            username="other",
            email="other@example.com",
            password=TEST_PASSWORD,
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
            "turns:activity_update",
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
            password=TEST_PASSWORD,
        )
        self.player = User.objects.create_user(
            username="player",
            email="player@example.com",
            password=TEST_PASSWORD,
        )
        self.other_player = User.objects.create_user(
            username="other",
            email="other@example.com",
            password=TEST_PASSWORD,
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
            "turns:activity_delete",
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


@override_settings(DEBUG=True)
class QueryCountTests(TestCase):
    """
    Verify views don't perform duplicate database queries.

    The dispatch() pattern in mixins intentionally duplicates lookups
    to avoid calling super().dispatch() multiple times, but should not
    result in double queries to the database.
    """

    def setUp(self):
        self.gm = User.objects.create_user(
            username="gm",
            email="gm@example.com",
            password=TEST_PASSWORD,
        )
        self.player = User.objects.create_user(
            username="player",
            email="player@example.com",
            password=TEST_PASSWORD,
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

    def test_turn_create_view_queries(self):
        """GMRequiredMixin should not double-query kingdom/membership."""
        self.client.force_login(self.gm)
        url = reverse("turns:turn_create", kwargs={"pk": self.kingdom.pk})

        # session, user, kingdom, membership
        # No extra queries - form doesn't need leadership roles on GET
        with self.assertNumQueries(4):
            response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_turn_detail_view_queries(self):
        """KingdomAccessMixin should efficiently load kingdom and activities."""
        ActivityLog.objects.create(
            kingdom=self.kingdom,
            turn=self.turn,
            activity_name="Test Activity",
            activity_trait=ActivityTrait.REGION,
            created_by=self.player,
        )
        self.client.force_login(self.player)
        url = reverse(
            "turns:turn_detail",
            kwargs={"pk": self.kingdom.pk, "turn_pk": self.turn.pk},
        )

        # session, user, kingdom, membership, turn, activities (with select_related), user again
        # Note: Extra user query from template checking activity.created_by
        with self.assertNumQueries(7):
            response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_activity_update_view_queries(self):
        """ActivityUpdateView dispatch() + get_object() results in some duplicate queries."""
        activity = ActivityLog.objects.create(
            kingdom=self.kingdom,
            turn=self.turn,
            activity_name="Test Activity",
            activity_trait=ActivityTrait.REGION,
            created_by=self.player,
        )
        self.client.force_login(self.player)
        url = reverse(
            "turns:activity_update",
            kwargs={"pk": self.kingdom.pk, "activity_pk": activity.pk},
        )

        # session, user, kingdom, membership, activity+turn (select_related),
        # then get_object() refetches: kingdom, activity, turn, leadership roles
        # Note: Could be optimized by caching get_object() result from dispatch()
        with self.assertNumQueries(9):
            response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_activity_delete_view_queries(self):
        """ActivityDeleteView should efficiently check permissions and delete."""
        activity = ActivityLog.objects.create(
            kingdom=self.kingdom,
            turn=self.turn,
            activity_name="Test Activity",
            activity_trait=ActivityTrait.REGION,
            created_by=self.player,
        )
        self.client.force_login(self.player)
        url = reverse(
            "turns:activity_delete",
            kwargs={"pk": self.kingdom.pk, "activity_pk": activity.pk},
        )

        # session, user, kingdom, membership, activity, user again, turn, delete
        # Note: Extra user query from can_be_modified_by checking created_by
        with self.assertNumQueries(8):
            response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
