from django import template
from wagtailcore.models import Locale

register = template.Library()


@register.filter
def get_translation_for_locale(obj, locale):
    """
    Get the translated version of a TranslatableMixin object for the given locale.
    Falls back to the original if translation doesn't exist.
    """
    if not hasattr(obj, 'translation_key') or not hasattr(obj, 'locale'):
        return obj
    
    # If already on correct locale, return as-is
    if obj.locale_id == locale.id:
        return obj
    
    # Try to get the translation
    try:
        translation = obj.__class__.objects.get(
            translation_key=obj.translation_key,
            locale=locale
        )
        return translation
    except obj.__class__.DoesNotExist:
        # Fallback to original if translation doesn't exist
        return obj
