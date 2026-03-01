from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.core.exceptions import ValidationError
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class BlogIndex(Page):
    template = "blogpages/blog_index_page.html"
    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['blogpages.BlogDetail']

    subtitle = models.CharField(max_length=255, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['blogpages'] = BlogDetail.objects.live(
        ).public()
        return context


class BlogDetailTags(TaggedItemBase):
    content_object = ParentalKey(
        'BlogDetail', related_name='tagged_items', on_delete=models.CASCADE)


class BlogDetail(Page):
    subtitle = models.CharField(max_length=255, blank=True)
    body = StreamField(
        [
            ('info', blocks.CharBlock(
                help_text="This is an info block. It can be used to display important information to the reader."
            )),
            ('faq', blocks.ListBlock(
                blocks.StructBlock([
                    ('question', blocks.CharBlock()),
                    ('answer', blocks.RichTextBlock(
                        features=['bold', 'italic', 'link'])),
                ])
            )),
            ('text', blocks.TextBlock()),
            ('image', ImageChooserBlock()),
            ('carousel', blocks.StreamBlock([
                ('image', ImageChooserBlock()),
                ('quotation', blocks.StructBlock([
                    ('text', blocks.TextBlock()),
                    ('author', blocks.TextBlock()),
                ])),
            ]))
        ],
        block_counts={
            'text': {'min_num': 1, 'max_num': 1},
            'image': {'min_num': 1, 'max_num': 2},
            'carousel': {'min_num': 0, 'max_num': 1},
        },
        use_json_field=True,
        blank=True,
        null=True,
    )
    tags = ClusterTaggableManager(through=BlogDetailTags, blank=True)

    parent_page_types = ['blogpages.BlogIndex']
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
        FieldPanel("tags"),
    ]

    def clean(self):
        super().clean()

        errors = {}

        if 'blog' in self.title.lower():
            errors['title'] = ValidationError(
                "The title cannot contain the word 'blog'."
            )

        if 'blog' in self.subtitle.lower():
            errors['subtitle'] = ValidationError(
                "The subtitle cannot contain the word 'blog'."
            )

        if 'blog' in self.slug.lower():
            errors['slug'] = ValidationError(
                "The slug cannot contain the word 'blog'."
            )

        if errors:
            raise ValidationError(errors)
