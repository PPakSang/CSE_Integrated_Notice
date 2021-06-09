from django.template.defaultfilters import register
from urllib.parse import unquote #python3

@register.filter
def unquote_new(value):
    return unquote(value)