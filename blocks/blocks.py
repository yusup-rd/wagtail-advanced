from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class TextBlock(blocks.TextBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs,
                         help_text="This is a text block. It can be used to display any text content to the reader."

                         )

    class Meta:
        template = "blocks/text_block.html"
        icon = "doc-full"
        group = "Standalone Blocks"


class ImageBlock(ImageChooserBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs,
                         help_text="This is an image block. It can be used to display images to the reader."
                         )

    class Meta:
        template = "blocks/image_block.html"


class InfoBlock(blocks.StaticBlock):
    class Meta:
        # icon = "..."
        # template = "..."
        admin_text = "This is an info block. It can be used to display important information to the reader."
        label = "General Information"


class FAQBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answer = blocks.RichTextBlock(features=['bold', 'italic', 'link'])


class FAQListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(FAQBlock(), **kwargs)

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

    class Meta:
        # icon = "..."
        template = "blocks/carousel_block.html"
        label = "Image Carousel"
