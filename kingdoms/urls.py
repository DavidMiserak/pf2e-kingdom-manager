from django.urls import path

from .views import (
    ActivityCreateView,
    ActivityDeleteView,
    ActivityUpdateView,
    JoinKingdomView,
    KingdomCreateView,
    KingdomDeleteView,
    KingdomDetailView,
    KingdomListView,
    KingdomMemberManageView,
    KingdomUpdateView,
    LeadershipUpdateView,
    RegenerateInviteView,
    SkillsUpdateView,
    TurnCompleteView,
    TurnCreateView,
    TurnDeleteView,
    TurnDetailView,
    TurnUpdateView,
    UpdateCharacterNameView,
)

app_name = "kingdoms"
urlpatterns = [
    path("", KingdomListView.as_view(), name="kingdom_list"),
    path("create/", KingdomCreateView.as_view(), name="kingdom_create"),
    path(
        "join/<uuid:invite_code>/",
        JoinKingdomView.as_view(),
        name="join",
    ),
    path("<int:pk>/", KingdomDetailView.as_view(), name="kingdom_detail"),
    path("<int:pk>/edit/", KingdomUpdateView.as_view(), name="kingdom_update"),
    path(
        "<int:pk>/character-name/",
        UpdateCharacterNameView.as_view(),
        name="update_character_name",
    ),
    path(
        "<int:pk>/delete/",
        KingdomDeleteView.as_view(),
        name="kingdom_delete",
    ),
    path(
        "<int:pk>/leadership/",
        LeadershipUpdateView.as_view(),
        name="leadership_update",
    ),
    path(
        "<int:pk>/skills/",
        SkillsUpdateView.as_view(),
        name="skills_update",
    ),
    path(
        "<int:pk>/members/",
        KingdomMemberManageView.as_view(),
        name="member_manage",
    ),
    path(
        "<int:pk>/members/regenerate-invite/",
        RegenerateInviteView.as_view(),
        name="regenerate_invite",
    ),
    # Turns
    path(
        "<int:pk>/turns/create/",
        TurnCreateView.as_view(),
        name="turn_create",
    ),
    path(
        "<int:pk>/turns/<int:turn_pk>/",
        TurnDetailView.as_view(),
        name="turn_detail",
    ),
    path(
        "<int:pk>/turns/<int:turn_pk>/edit/",
        TurnUpdateView.as_view(),
        name="turn_update",
    ),
    path(
        "<int:pk>/turns/<int:turn_pk>/delete/",
        TurnDeleteView.as_view(),
        name="turn_delete",
    ),
    path(
        "<int:pk>/turns/<int:turn_pk>/complete/",
        TurnCompleteView.as_view(),
        name="turn_complete",
    ),
    # Activities
    path(
        "<int:pk>/turns/<int:turn_pk>/activities/create/",
        ActivityCreateView.as_view(),
        name="activity_create",
    ),
    path(
        "<int:pk>/activities/<int:activity_pk>/edit/",
        ActivityUpdateView.as_view(),
        name="activity_update",
    ),
    path(
        "<int:pk>/activities/<int:activity_pk>/delete/",
        ActivityDeleteView.as_view(),
        name="activity_delete",
    ),
]
