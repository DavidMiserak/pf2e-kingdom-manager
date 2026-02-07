from django.urls import path

from .views import (
    ActivityCreateView,
    ActivityDeleteView,
    ActivityUpdateView,
    TurnCompleteView,
    TurnCreateView,
    TurnDeleteView,
    TurnDetailView,
    TurnUpdateView,
)

app_name = "turns"
urlpatterns = [
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
