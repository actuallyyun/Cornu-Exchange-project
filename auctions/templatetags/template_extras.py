import markdown2

from django import template
from django.template.defaultfilters import register, stringfilter

register = template.Library()


@register.filter
def convert_markdown(value):
    return markdown2.markdown(value)
