import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("kingdoms", "0012_move_leadership"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name="KingdomSkillProficiency",
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
                            "skill",
                            models.CharField(
                                choices=[
                                    ("agriculture", "Agriculture"),
                                    ("arts", "Arts"),
                                    ("boating", "Boating"),
                                    ("defense", "Defense"),
                                    ("engineering", "Engineering"),
                                    ("exploration", "Exploration"),
                                    ("folklore", "Folklore"),
                                    ("industry", "Industry"),
                                    ("intrigue", "Intrigue"),
                                    ("magic", "Magic"),
                                    ("politics", "Politics"),
                                    ("scholarship", "Scholarship"),
                                    ("statecraft", "Statecraft"),
                                    ("trade", "Trade"),
                                    ("warfare", "Warfare"),
                                    ("wilderness", "Wilderness"),
                                ],
                                max_length=12,
                            ),
                        ),
                        (
                            "proficiency",
                            models.CharField(
                                choices=[
                                    ("untrained", "Untrained"),
                                    ("trained", "Trained"),
                                    ("expert", "Expert"),
                                    ("master", "Master"),
                                    ("legendary", "Legendary"),
                                ],
                                default="untrained",
                                max_length=10,
                            ),
                        ),
                        (
                            "kingdom",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="skill_proficiencies",
                                to="kingdoms.kingdom",
                            ),
                        ),
                    ],
                    options={
                        "verbose_name_plural": "kingdom skill proficiencies",
                        "ordering": ["skill"],
                        "unique_together": {("kingdom", "skill")},
                        "db_table": "kingdoms_kingdomskillproficiency",
                    },
                ),
            ],
            database_operations=[],
        ),
    ]
