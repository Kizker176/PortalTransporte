
from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.fields import RichTextField
from wagtail.documents import get_document_model
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.blocks import PageChooserBlock
from wagtail.contrib.settings.models import (
    BaseSiteSetting,
    register_setting,
)
from wagtail.images import get_image_model
from wagtail.models import Site
from wagtail.snippets.models import register_snippet

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
        "home.ContactPage",
        "home.CentrosPage",
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

    mostrar_embebido = models.BooleanField(
        default=False,
        verbose_name="Mostrar contenido embebido"
    )

    titulo_embebido = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Título del contenido embebido"
    )

    url_embebida = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="URL del contenido embebido"
    )

    altura_embebido = models.PositiveIntegerField(
        default=800,
        verbose_name="Altura del contenido embebido (px)"
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("mostrar_embebido"),
        FieldPanel("titulo_embebido"),
        FieldPanel("url_embebida"),
    ]

    parent_page_types = [
        "home.HomePage",
        "home.SectionPage",
    ]

    subpage_types = [
        "home.HomePage",
        "home.StandardPage",
        "home.SectionPage",
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

    body = RichTextField(
        blank=True,
        verbose_name="Contenido"
    )

    documento = models.ForeignKey(
        get_document_model(),
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
        FieldPanel("body"),
        FieldPanel("documento"),
        FieldPanel("fecha_documento"),
    ]

    parent_page_types = ["home.SectionPage"]

class ContactPage(Page):
    """Página pública de contacto; envía los mensajes por correo electrónico."""

    intro = models.CharField(
        max_length=300,
        blank=True,
        default="Completa el formulario y nos pondremos en contacto contigo.",
        verbose_name="Texto introductorio",
    )

    aviso_privacidad_url = models.URLField(
        verbose_name="Enlace al aviso de privacidad",
        help_text="Introduce la URL pública del aviso de privacidad institucional.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("aviso_privacidad_url"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []

    template = "home/contact_page.html"

    def serve(self, request, *args, **kwargs):
        from django.conf import settings
        from django.contrib import messages
        from django.core.mail import EmailMessage
        from django.shortcuts import redirect, render
        from .forms import ContactoForm

        if request.method != "POST":
            return super().serve(request, *args, **kwargs)

        form = ContactoForm(request.POST)
        if form.is_valid():
            if not getattr(settings, "CONTACTO_DESTINO_EMAIL", "transporte_guanajuato@guanajuato.gob.mx"):
                messages.error(
                    request,
                    "El servicio de contacto no está configurado en este momento. "
                    "Por favor, inténtalo más tarde.",
                )
            else:
                datos = form.cleaned_data
                asunto = f"Nuevo mensaje de contacto del portal: {datos['nombre_completo']}"
                cuerpo = (
                    "Se recibió un nuevo mensaje desde el formulario Contáctanos.\n\n"
                    f"Nombre completo: {datos['nombre_completo']}\n"
                    f"Teléfono: {datos['telefono']}\n"
                    f"Municipio: {datos['municipio']}\n"
                    f"Correo electrónico: {datos['correo']}\n\n"
                    "Descripción del mensaje:\n"
                    f"{datos['mensaje']}\n\n"
                    "La persona marcó la casilla de lectura del aviso de privacidad."
                )
                try:
                    email = EmailMessage(
                        subject=asunto,
                        body=cuerpo,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[settings.CONTACTO_DESTINO_EMAIL],
                        reply_to=[datos["correo"]],
                    )
                    email.send(fail_silently=False)
                except Exception:
                    import logging
                    logging.getLogger(__name__).exception(
                        "No se pudo enviar el formulario de contacto."
                    )
                    messages.error(
                        request,
                        "No fue posible enviar tu mensaje. Inténtalo más tarde.",
                    )
                else:
                    messages.success(
                        request,
                        "Tu mensaje fue enviado correctamente. Gracias por contactarnos.",
                    )
                    return redirect(self.url)

        context = self.get_context(request, *args, **kwargs)
        context["form"] = form
        return render(request, self.get_template(request), context)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        from .forms import ContactoForm
        context.setdefault("form", ContactoForm())
        return context

@register_snippet
class Centro(models.Model):
    """Catálogo de centros de atención del PortalTransporte."""

    municipio = models.CharField(
            max_length=100,
            verbose_name="Municipio",
    )

    clave_revista = models.CharField(
                max_length=100,
                verbose_name="Clave",
    )
    
    nombre = models.CharField(
        max_length=350,
        verbose_name="Nombre del centro",
    )

    domicilio = models.CharField(
        max_length=350,
        verbose_name="Domicilio",
    )

    telefono = models.CharField(
        max_length=20,
        verbose_name="Teléfono",
    )

    panels = [
        FieldPanel("municipio"),
        FieldPanel("clave_revista"),
        FieldPanel("nombre"),
        FieldPanel("domicilio"),
        FieldPanel("telefono"),
    ]

    class Meta:
        verbose_name = "Centro"
        verbose_name_plural = "Centros"
        ordering = ["municipio", "nombre"]

    def __str__(self):
        return self.nombre

class CentrosPage(Page):
    """Página pública que lista los centros registrados en el catálogo."""

    intro = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Introducción",
    )

    body = RichTextField(
        blank=True,
        verbose_name="Contenido"
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    parent_page_types = ["home.HomePage", "home.CentrosPage"]
    subpage_types = [
        "home.StandardPage",
        "home.DocumentPage",
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["centros"] = Centro.objects.all().order_by("municipio", "nombre")
        return context