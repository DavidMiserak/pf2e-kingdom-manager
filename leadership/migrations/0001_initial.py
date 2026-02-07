import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("kingdoms", "0011_activitylog_kingdoms_ac_turn_id_731fbc_idx_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name="LeadershipAssignment",
                    fields=[
                        (
                            "id",
                            models.BigAutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        ),
                        (
                            "role",
                            models.CharField(
                                choices=[
                                    ("ruler", "Ruler"),
                                    ("counselor", "Counselor"),
                                    ("general", "General"),
                                    ("emissary", "Emissary"),
                                    ("magister", "Magister"),
                                    ("treasurer", "Treasurer"),
                                    ("viceroy", "Viceroy"),
                                    ("warden", "Warden"),
                                ],
                                max_length=10,
                            ),
                        ),
                        (
                            "character_name",
                            models.CharField(blank=True, default="", max_length=100),
                        ),
                        ("is_pc", models.BooleanField(default=True)),
                        ("is_invested", models.BooleanField(default=False)),
                        ("is_vacant", models.BooleanField(default=True)),
                        ("downtime_fulfilled", models.BooleanField(default=True)),
                        (
                            "kingdom",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="leadership_assignments",
                                to="kingdoms.kingdom",
                            ),
                        ),
                        (
                            "user",
                            models.ForeignKey(
                                blank=True,
                                null=True,
                                on_delete=django.db.models.deletion.SET_NULL,
                                related_name="leadership_assignments",
                                to=settings.AUTH_USER_MODEL,
                            ),
                        ),
                    ],
                    options={
                        "ordering": ["role"],
                        "unique_together": {("kingdom", "role")},
                        "db_table": "kingdoms_leadershipassignment",
                    },
                ),
            ],
            database_operations=[],
        ),
    ]
