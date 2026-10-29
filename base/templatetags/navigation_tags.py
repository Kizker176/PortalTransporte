
from django import template

from base.models import FooterText

register = template.Library()


@register.inclusion_tag(
    "home/includes/footer_text.html",
    takes_context=True,
)
def get_footer_text(context):
    footer = FooterText.objects.filter(live=True).first()

    return {
        "footer": footer,
    }
