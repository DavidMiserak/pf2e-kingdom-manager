from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("kingdoms", "0013_move_skills"),
        ("turns", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name="ActivityLog",
                ),
                migrations.DeleteModel(
                    name="KingdomTurn",
                ),
            ],
            database_operations=[],
        ),
    ]
