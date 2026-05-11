from django.db import migrations


def forwards(apps, schema_editor):
    Site = apps.get_model("wagtailcore", "Site")
    SocialMediaLinks = apps.get_model("settings", "SocialMediaLinks")

    site = Site.objects.first()
    if site is None:
        return

    for obj in SocialMediaLinks.objects.filter(site__isnull=True):
        obj.site = site
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("settings", "0003_add_site_nullable"),
    ]

    operations = [
        migrations.RunPython(forwards, reverse_code=migrations.RunPython.noop),
    ]
