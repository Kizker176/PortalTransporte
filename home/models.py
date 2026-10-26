
from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.fields import RichTextField


class HomePage(Page):
    subtitulo = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    banners = StreamField(
        [
            (
                "banner",
                blocks.StructBlock(
                    [
                        ("titulo", blocks.CharBlock(max_length=200)),
                        (
                            "descripcion",
                            blocks.TextBlock(required=False)
                        ),
                        (
                            "imagen",
                            ImageChooserBlock()
                        ),
                        (
                            "texto_boton",
                            blocks.CharBlock(required=False)
                        ),
                        (
                            "enlace_boton",
                            blocks.URLBlock(required=False)
                        ),
                    ]
                )
            )
        ],
        blank=True,
        use_json_field=True
    )

    menu_lateral = StreamField(
        [
            (
                "enlace",
                blocks.StructBlock(
                    [
                        (
                            "titulo",
                            blocks.CharBlock(
                                max_length=100,
                                label="Nombre del enlace"
                            )
                        ),
                        (
                            "url",
                            blocks.URLBlock(
                                label="URL del enlace"
                            )
                        ),
                        (
                            "abrir_nueva_pestana",
                            blocks.BooleanBlock(
                                required=False,
                                default=False,
                                label="Abrir en nueva pestaña"
                            )
                        ),
                    ],
                    label="Enlace del menú"
                )
            )
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Menú lateral"
    )

    servicios = StreamField(
        [
            (
                "servicio",
                blocks.StructBlock(
                    [
                        ("nombre", blocks.CharBlock(max_length=120)),
                        (
                            "descripcion",
                            blocks.TextBlock(required=False)
                        ),
                        (
                            "imagen",
                            ImageChooserBlock(required=False)
                        ),
                        (
                            "enlace",
                            blocks.URLBlock(required=False)
                        ),
                    ]
                )
            )
        ],
        blank=True,
        use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitulo"),
        FieldPanel("banners"),
        FieldPanel("servicios"),
        FieldPanel("menu_lateral"),
    ]

    # La portada puede contener páginas informativas.
    subpage_types = [
        "home.StandardPage",
        "home.NoticiaPage",
    ]

class StandardPage(Page):
    intro = models.CharField(
        max_length=300,
        blank=True
    )

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    parent_page_types = ["home.HomePage"]


class NoticiaPage(Page):
    imagen = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    fecha_publicacion = models.DateField(
        null=True,
        blank=True
    )

    resumen = models.CharField(
        max_length=300,
        blank=True
    )

    contenido = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("imagen"),
        FieldPanel("fecha_publicacion"),
        FieldPanel("resumen"),
        FieldPanel("contenido"),
    ]

    parent_page_types = ["home.HomePage"]

def get_context(self, request, *args, **kwargs):
    context = super().get_context(request, *args, **kwargs)

    context["noticias"] = (
        NoticiaPage.objects
        .child_of(self)
        .live()
        .order_by("-fecha_publicacion", "-first_published_at")[:4]
    )

    return context