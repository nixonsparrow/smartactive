from django.db import models
from wagtail.admin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                         PageChooserPanel, StreamFieldPanel)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from manager import blocks


class HomePage(Page):
    """Home page model"""

    template = 'home/home_page.html'
    max_count = 1

    banner_title = models.CharField(max_length=100, null=True, blank=False)
    banner_subtitle = RichTextField(features=['bold', 'italic'], null=True, blank=False)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content = StreamField(
        [
            ('title_and_text', blocks.TitleAndTextBlock()),
            ('full_richtext', blocks.RichTextBlock()),
            ('simple_richtext', blocks.SimpleRichTextBlock()),
            ('cards', blocks.CardBlock()),
            ('cta', blocks.CTABlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('banner_title'),
                FieldPanel('banner_subtitle'),
                ImageChooserPanel('banner_image'),
                PageChooserPanel('banner_cta'),
            ], heading='Banner'
        ),
        StreamFieldPanel('content'),
    ]

    class Meta:

        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
