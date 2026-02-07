from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("kingdoms", "0012_move_leadership"),
        ("skills", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name="KingdomSkillProficiency",
                ),
            ],
            database_operations=[],
        ),
    ]
