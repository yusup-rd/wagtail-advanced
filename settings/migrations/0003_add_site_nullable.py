from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("settings", "0002_socialmedialinks"),
    ]

    operations = [
        migrations.AddField(
            model_name="socialmedialinks",
            name="site",
            field=models.ForeignKey(
                to="wagtailcore.Site",
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                related_name="+",
            ),
        ),
    ]
