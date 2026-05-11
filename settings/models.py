from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting, BaseSiteSetting, register_setting


@register_setting
class GenericFooterText(BaseGenericSetting):
    text = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("text"),
    ]


@register_setting
class SocialMediaLinks(BaseSiteSetting):
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    panels = [
        FieldPanel("twitter"),
        FieldPanel("facebook"),
        FieldPanel("instagram"),
    ]
