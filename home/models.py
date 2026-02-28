from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string
from wagtail.documents import get_document_model_string
from django.core.exceptions import ValidationError


class HomePage(Page):
    template = "home/home_page.html"
    max_count = 1

    subtitle = models.CharField(max_length=100, blank=True, null=True)
    content = RichTextField(blank=True)

    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    custom_document = models.ForeignKey(
        get_document_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    cta_url = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    cta_external_url = models.URLField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('cta_url'),
        FieldPanel('cta_external_url'),
        FieldPanel('content'),
        FieldPanel('image'),
        FieldPanel('custom_document'),
    ]

    @property
    def cta_urls(self):
        if self.cta_url:
            return self.cta_url.url
        if self.cta_external_url:
            return self.cta_external_url
        else:
            return None

    def clean(self):
        super().clean()

        if self.cta_url and self.cta_external_url:
            raise ValidationError(
                "You cannot have both an internal and external CTA URL."
            )
