from django import template
from django.utils.html import escape

register = template.Library()

@register.filter(name='add_attrs')
def add_attrs(field, attr_string):
    attrs = dict(attr.split('=') for attr in attr_string.split(','))
    widget = field.field.widget
    for attr, value in attrs.items():
        widget.attrs[attr] = escape(value)
    return field
