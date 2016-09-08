from django import template
from ..forms import LoginForm

register = template.Library()

@register.filter(name='quote')
def quote(value):
    return '"'+value+'"'
