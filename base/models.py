
from django.db import models

from wagtail.admin.panels import FieldPanel, PublishingPanel
from wagtail.fields import RichTextField
from wagtail.models import (
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
)
from wagtail.snippets.models import register_snippet

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.admin.panels import (   
    FieldPanel,
    InlinePanel,
    PublishingPanel,
)
from wagtail.models import (
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
    Orderable,
)


@register_snippet
class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    ClusterableModel,
):
    # body = RichTextField(
    #     blank=True,
    #     verbose_name="Contenido del footer",
    # )
    
    logo_izquierdo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Primer logotipo",
    )

    logo_derecho = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Segundo logotipo",
    )

    panels = [
        InlinePanel(
            "secciones_footer",
            label="Secciones del footer",
        ),
        FieldPanel("logo_izquierdo"),
        FieldPanel("logo_derecho"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Footer institucional"

    def get_preview_template(self, request, mode_name):
        return "home/base.html"

    def get_preview_context(self, request, mode_name):
        # return {"footer_text": self.body}
        return {"footer": self}

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Footer"
        verbose_name_plural = "Footer"

class FooterSeccion(Orderable,ClusterableModel):
    footer = ParentalKey(
        "base.FooterText",
        on_delete=models.CASCADE,
        related_name="secciones_footer",
    )

    TIPOGRAFIAS = [
            ("Arial, sans-serif", "Arial"),
            ("Cursiva, cursive", "Cursiva"),
            ("Monospace, monospace", "Monospace"),
        ]

    tipografia_titulo = models.CharField(
        max_length=100,
        choices=TIPOGRAFIAS,
        blank=True,
        verbose_name="Tipografía del título",
    )

    tamano_titulo = models.PositiveIntegerField(
        default=20,
        blank=True,
        verbose_name="Tamaño del título (px)",
    )

    titulo = models.CharField(
        max_length=150,
        verbose_name="Título de la sección",
    )

    panels = [
        FieldPanel("titulo"),
        InlinePanel(
            "enlaces",
            label="Enlaces de esta sección",
        ),
        FieldPanel("tipografia_titulo"),
        FieldPanel("tamano_titulo")

    ]

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Sección del footer"
        verbose_name_plural = "Secciones del footer"
        ordering = ["sort_order"]


class FooterEnlace(Orderable):
    seccion = ParentalKey(
        "base.FooterSeccion",
        on_delete=models.CASCADE,
        related_name="enlaces",
    )

    titulo = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Título del enlace",
    )

    url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="URL del enlace",
    )
    TIPOGRAFIAS = [
        ("Arial, sans-serif", "Arial"),
        ("Cursiva, cursive", "Cursiva"),
        ("Monospace, monospace", "Monospace"),
    ]

    ICONOS = [
        ("fa-solid fa-chevron-right", "Flecha"),
        ("fa-solid fa-folder-open", "Directorio"),
        ("fa-solid fa-sitemap", "Estructura orgánica"),
        ("fa-solid fa-money-bill-wave", "Sueldos"),
        ("fa-solid fa-chart-column", "Indicadores"),
        ("fa-solid fa-clipboard-check", "Auditorías"),
        ("fa-solid fa-file-circle-check", "Solicitudes"),
        ("fa-solid fa-file-invoice", "Cuenta pública"),
        ("fa-solid fa-shield-halved", "Privacidad"),
        ("fa-solid fa-users", "Atención ciudadana"),
        ("fa-solid fa-envelope", "Correo"),
        ("fa-solid fa-phone", "Teléfono"),
        ("fa-solid fa-location-dot", "Ubicación"),
        ("fa-solid fa-scale-balanced", "Legalizaciones"),
        ("fa-brands fa-facebook", "Facebook"),
        ("fa-brands fa-x-twitter", "X / Twitter"),
        ("fa-brands fa-instagram", "Instagram"),
    ]

    tipografia = models.CharField(
        max_length=100,
        choices=TIPOGRAFIAS,
        blank=True,
        default="Arial, sans-serif",
        verbose_name="Tipografía del enlace",
    )

    tamano_letra = models.PositiveSmallIntegerField(
        default=16,
        blank=True,
        verbose_name="Tamaño de letra (px)",
    )

    icono = models.CharField(
        max_length=100,
        choices=ICONOS,
        blank=True,
        default="fa-solid fa-chevron-right",
        verbose_name="Icono del enlace",
    )

    panels = [
        FieldPanel("titulo"),
        FieldPanel("url"),
        FieldPanel("icono"),
        FieldPanel("tipografia"),
        FieldPanel("tamano_letra"),
    ]

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Enlace del footer"
        verbose_name_plural = "Enlaces del footer"
        ordering = ["sort_order"]
