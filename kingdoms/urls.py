from django.urls import path

from .views import (
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
]
