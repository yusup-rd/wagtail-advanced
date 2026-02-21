from django.db import models
from wagtail.documents.models import AbstractDocument, Document


class CustomDocument(AbstractDocument):
    description = models.TextField(blank=True, max_length=255)

    admin_form_fields = Document.admin_form_fields + ("description",)
