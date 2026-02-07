from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("kingdoms", "0011_activitylog_kingdoms_ac_turn_id_731fbc_idx_and_more"),
        ("leadership", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name="LeadershipAssignment",
                ),
            ],
            database_operations=[],
        ),
    ]
