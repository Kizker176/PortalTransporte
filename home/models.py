
from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.fields import RichTextField
from wagtail.documents import get_document_model_string
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.blocks import PageChooserBlock
from wagtail.contrib.settings.models import (
    BaseSiteSetting,
    register_setting,
)
from wagtail.images import get_image_model
from wagtail.models import Site

class BannerBlock(blocks.StructBlock):
        imagen = ImageChooserBlock(
            label="Imagen del banner"
        )
        titulo = blocks.CharBlock(
            max_length=150,
            required=False,
            label="Título"
        )
        descripcion = blocks.TextBlock(
            required=False,
            label="Descripción"
        )
        texto_boton = blocks.CharBlock(
            max_length=50,
            required=False,
            label="Texto del botón"
        )
        enlace_boton = blocks.URLBlock(
            required=False,
            label="Enlace del botón"
        )

class Meta:
        label = "Banner"
        icon = "image"

@register_setting
class ConfiguracionSitio(BaseSiteSetting):
    """ nombre_institucion = models.CharField(
        max_length=200,
        default="Secretaría de Gobierno",
        verbose_name="Nombre de la institución",
    ) """

    texto_encabezado = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Texto del encabezado",
    )

    logo = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Logo principal",
    )

    logo_movil = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Logo para móviles",
    )

    escudo = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Escudo institucional",
    )

    texto_pie = models.TextField(
        blank=True,
        verbose_name="Texto del pie de página",
    )

    panels = [
        FieldPanel("texto_encabezado"),
        FieldPanel("logo"),
        FieldPanel("logo_movil"),
        FieldPanel("escudo"),
        FieldPanel("texto_pie"),
    ]

    class Meta:
        verbose_name = "Configuración del sitio"
        verbose_name_plural = "Configuración del sitio"

class HomePage(Page):
    subtitulo = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    banners = StreamField(
        [
            ("banner", BannerBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Carrusel de banners",
    )

    menu_lateral = StreamField(
        [
            (
                "pagina",
                blocks.StructBlock(
                    [
                        (
                            "pagina",
                            PageChooserBlock(
                                label="Seleccionar página"
                            )
                        ),
                        (
                            "titulo_personalizado",
                            blocks.CharBlock(
                                required=False,
                                max_length=100,
                                label="Título personalizado"
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
                    ]
                )
            ),
            (
                "enlace_externo",
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
                                label="URL externa"
                            )
                        ),
                    ]
                )
            ),
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
        "home.SectionPage",
        "home.NewsIndexPage",
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["noticias"] = (
            NoticiaPage.objects
            .child_of(self)
            .live()
            .order_by("-fecha_publicacion", "-first_published_at")[:4]
        )

        return context
    
    def menu_principal(request):
        site = Site.find_for_request(request)

        if site is None:
            return {"menu_items": []}

        menu_items = (
            site.root_page
            .get_children()
            .live()
            .in_menu()
        )

        return {"menu_items": menu_items}


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


class SectionPage(Page):
    """
    Páginas principales como Conócenos, Servicios y Transparencia.
    """

    intro = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Introducción"
    )

    body = RichTextField(
        blank=True,
        verbose_name="Contenido"
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    parent_page_types = [
        "home.HomePage",
        "home.SectionPage",
    ]

    subpage_types = [
        "home.StandardPage",
        "home.DocumentPage",
    ]


class NewsIndexPage(Page):
    """
    Página que muestra el listado de noticias.
    """

    intro = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Introducción"
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["home.HomePage"]

    subpage_types = ["home.NoticiaPage"]


class DocumentPage(Page):
    """
    Página para publicar un documento descargable.
    """

    descripcion = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Descripción"
    )

    documento = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Archivo descargable"
    )

    fecha_documento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha del documento"
    )

    content_panels = Page.content_panels + [
        FieldPanel("descripcion"),
        FieldPanel("documento"),
        FieldPanel("fecha_documento"),
    ]

    parent_page_types = ["home.SectionPage"]