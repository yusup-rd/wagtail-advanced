from django.db import models
from wagtail.models import Orderable, Page, ParentalKey
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel, FieldRowPanel, HelpPanel, MultipleChooserPanel, TitleFieldPanel
from wagtail.images import get_image_model_string
from wagtail.documents import get_document_model_string
from django.core.exceptions import ValidationError


class HomePageGalleryImage(Orderable):
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE,
                       related_name='gallery_images')
    image = models.ForeignKey(
        get_image_model_string(),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='+'
    )

    panels = [
        FieldPanel('image'),
    ]


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
        MultiFieldPanel([
            HelpPanel(
                content="You can add a subtitle, content, an image, and a call-to-action (CTA) link. The CTA can be either an internal page or an external URL, but not both.",
                heading="Note:"
            ),
            TitleFieldPanel(
                "subtitle", help_text="A short description or tagline for the homepage.", placeholder="Welcome to our website!"),
            FieldRowPanel([
                PageChooserPanel('cta_url', 'blogpages.BlogDetail',
                                 help_text="Choose an internal page for the CTA link.", heading="Internal CTA Link"),
                FieldPanel('cta_external_url',
                           help_text="Enter an external URL for the CTA link.", heading="External CTA Link"),
            ],
                help_text="You can only have one CTA link. If you choose an internal page, leave the external URL blank, and vice versa.",
                heading="Call-to-Action (CTA) Links"
            ),
        ], heading="Homepage Content"),

        # InlinePanel(
        #     'gallery_images', label="Gallery Images", help_text="Add images to the homepage gallery.", min_num=2, max_num=5
        # )
        MultipleChooserPanel(
            'gallery_images', label="Gallery Images", help_text="Add images to the homepage gallery.", min_num=2, max_num=5, chooser_field_name='image'
        )


        # FieldPanel('subtitle'),
        # FieldPanel('cta_url'),
        # FieldPanel('cta_external_url'),
        # FieldPanel('content'),
        # FieldPanel('image'),
        # FieldPanel('custom_document'),
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
