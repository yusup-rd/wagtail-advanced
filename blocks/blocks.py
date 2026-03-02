from django.core.exceptions import ValidationError
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class TextBlock(blocks.TextBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs,
                         help_text="This is a text block. It can be used to display any text content to the reader."

                         )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["text"] = value
        context["char_count"] = len(value or "")
        return context

    def clean(self, value):
        value = super().clean(value)
        if 'wordpress' in value.lower():
            raise ValidationError(
                "The word 'WordPress' is not allowed in this text block.")
        if len(value) < 10:
            raise ValidationError("Text must be at least 10 characters long.")
        if len(value) > 2000:
            raise ValidationError("Text must not exceed 2000 characters.")
        return value

    class Meta:
        template = "blocks/text_block.html"
        icon = "doc-full"
        group = "Standalone Blocks"


class ImageBlock(ImageChooserBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs,
                         help_text="This is an image block. It can be used to display images to the reader."
                         )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["image"] = value
        context["has_image"] = value is not None
        return context

    def clean(self, value):
        value = super().clean(value)
        if value is None:
            raise ValidationError("Please select an image.")
        return value

    class Meta:
        template = "blocks/image_block.html"


class InfoBlock(blocks.StaticBlock):
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["message"] = self.meta.admin_text
        return context

    class Meta:
        # icon = "..."
        # template = "..."
        admin_text = "This is an info block. It can be used to display important information to the reader."
        label = "General Information"


class FAQBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answer = blocks.RichTextBlock(features=['bold', 'italic', 'link'])

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        question = value.get("question", "") if value else ""
        context["question"] = question
        context["answer"] = value.get("answer") if value else ""
        context["question_anchor"] = question.strip().lower().replace(" ", "-")
        return context

    def clean(self, value):
        value = super().clean(value)
        errors = {}
        question = value.get("question", "") if value else ""
        if len(question) < 5:
            errors["question"] = ValidationError(
                "Question must be at least 5 characters long.")
        if len(question) > 200:
            errors["question"] = ValidationError(
                "Question must not exceed 200 characters.")
        if errors:
            raise blocks.StructBlockValidationError(block_errors=errors)
        return value


class FAQListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(FAQBlock(), **kwargs)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["faqs"] = value
        context["faq_count"] = len(value or [])
        return context

    def clean(self, value):
        value = super().clean(value)
        errors = {}
        seen_questions = []
        for i, faq in enumerate(value):
            question = faq.get("question", "").strip().lower()
            if question in seen_questions:
                errors[i] = ValidationError(
                    "Duplicate question: each FAQ must have a unique question.")
            else:
                seen_questions.append(question)
        if errors:
            raise blocks.ListBlockValidationError(block_errors=errors)
        return value

    class Meta:
        # icon = "..."
        template = "blocks/faq_list_block.html"
        min_num = 1
        max_num = 5
        label = "Frequently Asked Questions"


class CarouselBlock(blocks.StreamBlock):
    image = ImageChooserBlock()
    quotation = blocks.StructBlock([
        ('text', blocks.TextBlock()),
        ('author', blocks.TextBlock()),
    ])

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["slides"] = value
        context["slide_count"] = len(value or [])
        return context

    def clean(self, value):
        value = super().clean(value)
        image_slides = [
            block for block in value if block.block_type == "image"]
        if not image_slides:
            raise blocks.StreamBlockValidationError(
                non_block_errors=[ValidationError(
                    "The carousel must contain at least one image.")]
            )
        return value

    class Meta:
        # icon = "..."
        template = "blocks/carousel_block.html"
        label = "Image Carousel"
