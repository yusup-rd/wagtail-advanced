from wagtail.admin.panels import FieldPanel, mark_safe
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from taggit.models import Tag
from django.core.cache import cache
from django.contrib.auth.models import Permission
from wagtail import hooks
from blogpages.models import Author
from wagtail.admin.ui.components import Component
from wagtail.admin.site_summary import SummaryItem


@register_snippet
class TagViewSet(SnippetViewSet):
    model = Tag
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Tags"
    menu_order = 200
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]


@register_snippet
class AuthorSnippet(SnippetViewSet):
    model = Author
    icon = "user"
    add_to_admin_menu = True
    panels = [
        FieldPanel("name", permission="blogpages.can_edit_author_name"),
        FieldPanel("bio"),
    ]


@hooks.register('after_publish_page')
def delete_all_cache(request, page):
    # cache.clear()
    print("Cache cleared after publishing page: ", page.title)


@hooks.register('register_permissions')
def register_author_permissions():
    return Permission.objects.filter(
        content_type__app_label='blogpages',
        codename='can_edit_author_name',
    )


class WelcomePanel(Component):
    order = 10
    template_name = "panels/welcome_panel.html"

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        context['request'] = parent_context['request']
        context['username'] = parent_context['request'].user.username
        return context

    class Media:
        css = {
            'all': ['css/welcome_panel.css']
        }


@hooks.register('construct_homepage_panels')
def add_welcome_panel(request, panels):
    panels.append(WelcomePanel())


class HomepageSummaryItem(SummaryItem):
    order = 200
    template_name = "panels/summary_item.html"

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        context['purchases'] = 1000
        return context


@hooks.register('construct_homepage_summary_items')
def add_homepage_summary_item(request, items):
    items.append(HomepageSummaryItem(request))
