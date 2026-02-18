from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string


class HomePage(Page):
    template = "home/home_page.html"

    subtitle = models.CharField(max_length=100, blank=True, null=True)
    content = RichTextField(blank=True)

    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('content'),
        FieldPanel('image'),
    ]
