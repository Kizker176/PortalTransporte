from wagtail.embeds.finders.base import AbstractEmbedFinder

class CustomIframeFinder(AbstractEmbedFinder):
    def accept(self, url):
        # Puedes filtrar para que aplique solo a esta URL o retornar True si quieres permitir cualquier URL externa
        return "tramitesyservicios.guanajuato.gob.mx" in url

    def find_embed(self, url, max_width=None, max_height=None):
        return {
            'title': 'Trámites y Servicios Guanajuato',
            'author_name': '',
            'provider_name': 'Gobierno de Guanajuato',
            'type': 'rich',
            'version': '1.0',
            # Aquí defines el ancho, alto y estilos del iframe que se inyectará
            'html': f'<iframe src="{url}" width="100%" height="700px" style="border:none; border-radius: 8px;"></iframe>',
        }