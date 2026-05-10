from django.db import models
from wagtail.models import Page, DraftStateMixin, RevisionMixin, LockableMixin, PreviewableMixin, TranslatableMixin
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, PublishingPanel
from django.core.exceptions import ValidationError
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.fields import StreamField
from blocks import blocks as custom_blocks
from django.contrib.contenttypes.fields import GenericRelation
from wagtail.search import index
from wagtail.contrib.routable_page.models import RoutablePageMixin, path, re_path
from django.http import JsonResponse
from wagtail.api import APIField
from rest_framework.fields import Field


class BlogIndex(RoutablePageMixin, Page):
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

    def get_sitemap_urls(self, request=None):
        sitemap = super().get_sitemap_urls(request)
        last_mod = BlogDetail.objects.live().public().order_by('-last_published_at').first()
        sitemap.append({
            'location': self.get_full_url(request) + self.reverse_subpage('all'),
            'lastmod': (last_mod.last_published_at or last_mod.latest_revision_created_at),
        })
        sitemap.append({
            'location': self.get_full_url(request) + self.reverse_subpage('tag', args=['wagtail']),
            'lastmod': (last_mod.last_published_at or last_mod.latest_revision_created_at),
        })
        return sitemap

    @path('all/', name='all')
    def all_blogposts(self, request):
        posts = BlogDetail.objects.live().public()
        return self.render(request, context_overrides={'posts': posts})

    @path('tag/<slug:tag>/', name='tag')
    @path('tags/<slug:tag>/', name='tags')
    def blogposts_by_tag(self, request, tag):
        posts = BlogDetail.objects.live().public().filter(tags__slug=tag)

        if not tag:
            ...  # Redirect in here

        return self.render(request, context_overrides={'posts': posts})

    @re_path(r'^api/(\d+)/$', name='api')
    def api_response(self, request, year):
        posts = BlogDetail.objects.live().public().filter(first_published_at__year=year)
        return JsonResponse({
            'year': year,
            'posts': [post.title for post in posts]
        })

    def get_context(self, request):
        context = super().get_context(request)
        context['blogpages'] = BlogDetail.objects.live(
        ).public()
        return context


class BlogDetailTags(TaggedItemBase):
    content_object = ParentalKey(
        'BlogDetail', related_name='tagged_items', on_delete=models.CASCADE)


class AuthorSerializer(Field):
    def to_representation(self, value):
        return {
            'name': value.name,
            'bio': value.bio,
        }


class BlogDetail(Page):
    subtitle = models.CharField(max_length=255, blank=True)
    body = StreamField(
        [
            ('info', custom_blocks.InfoBlock()),
            ('faq', custom_blocks.FAQListBlock()),
            ('text', custom_blocks.TextBlock()),
            ('image', custom_blocks.ImageBlock()),
            ('carousel', custom_blocks.CarouselBlock())
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
    author = models.ForeignKey(
        'blogpages.Author',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    parent_page_types = ['blogpages.BlogIndex']
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("author", permission="home.add_author"),
        FieldPanel("subtitle"),
        FieldPanel("body"),
        FieldPanel("tags"),
    ]

    api_fields = [
        APIField("subtitle"),
        APIField("author", serializer=AuthorSerializer()),
        APIField("tags"),
        APIField("body"),
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


class Author(TranslatableMixin, LockableMixin, index.Indexed, DraftStateMixin, PreviewableMixin, RevisionMixin, models.Model):
    name = models.CharField(max_length=100)
    bio = RichTextField()
    revisions = GenericRelation(
        'wagtailcore.Revision', related_query_name='author')
    panels = [
        FieldPanel("name"),
        FieldPanel("bio"),
        PublishingPanel(),
    ]

    search_fields = [
        index.SearchField('name'),
        index.FilterField('name'),
        index.AutocompleteField('name'),
    ]

    def __str__(self):
        return self.name

    @property
    def preview_modes(self):
        return PreviewableMixin.DEFAULT_PREVIEW_MODES + [
            ('dark_mode', 'Dark Mode'),
        ]

    def get_preview_template(self, request, mode_name):
        templates = {
            "": "includes/author.html",
            'dark_mode': 'includes/author_dark_mode.html',
        }
        return templates.get(mode_name, templates[""])

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        if mode_name == 'dark_mode':
            context['warning'] = "You're in dark mode preview!"

        return context

    class Meta(TranslatableMixin.Meta):
        permissions = [
            ("can_edit_author_name", "Can edit author name"),
        ]
