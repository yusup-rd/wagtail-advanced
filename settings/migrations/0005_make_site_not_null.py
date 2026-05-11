from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("settings", "0004_backfill_site"),
    ]

    operations = [
        migrations.AlterField(
            model_name="socialmedialinks",
            name="site",
            field=models.ForeignKey(
                to="wagtailcore.Site",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
            ),
        ),
    ]
