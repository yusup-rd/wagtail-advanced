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


class FAQListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(FAQBlock(), **kwargs)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["faqs"] = value
        context["faq_count"] = len(value or [])
        return context

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

    class Meta:
        # icon = "..."
        template = "blocks/carousel_block.html"
        label = "Image Carousel"
