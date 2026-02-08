"""
Root URL configuration for all kingdom-related apps.

Mounts kingdoms, leadership, skills, and turns under the /kingdoms/ prefix.
"""

from django.urls import include, path

urlpatterns = [
    path("", include(("kingdoms.urls_core", "kingdoms"))),
    path("", include(("leadership.urls", "leadership"))),
    path("", include(("skills.urls", "skills"))),
    path("", include(("turns.urls", "turns"))),
]
