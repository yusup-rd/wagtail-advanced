from wagtail.models import Page


def site_settings(request):
    return {
        "navbar_pages": Page.objects.live().in_menu().public(),
    }
