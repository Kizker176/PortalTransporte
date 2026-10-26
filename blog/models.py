from django.db import models

# Create your models here.
from wagtail.models import Page
from wagtail.fields import RichTextField
from django.utils import timezone


class BlogPage(Page):
    date = models.DateField("Post date", default=timezone.localdate)
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + ["date", "intro", "body"]