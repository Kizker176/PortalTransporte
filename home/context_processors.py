from wagtail.models import Site


def menu_principal(request):
    """
    Devuelve las páginas publicadas marcadas para mostrarse en el menú
    que son hijas directas de la raíz del sitio actual.
    """
    site = Site.find_for_request(request)

    if site is None:
        return {"menu_items": []}

    menu_items = (
        site.root_page.get_children()
        .live()
        .in_menu()
    )

    return {"menu_items": menu_items}
