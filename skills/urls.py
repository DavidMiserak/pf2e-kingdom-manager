from django.urls import path

from .views import SkillsUpdateView

app_name = "skills"
urlpatterns = [
    path(
        "<int:pk>/skills/",
        SkillsUpdateView.as_view(),
        name="skills_update",
    ),
]
