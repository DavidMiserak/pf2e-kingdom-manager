from django.urls import path

from .views import LeadershipUpdateView

app_name = "leadership"
urlpatterns = [
    path(
        "<int:pk>/leadership/",
        LeadershipUpdateView.as_view(),
        name="leadership_update",
    ),
]
