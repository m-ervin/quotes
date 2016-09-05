from django import template
from ..forms import LoginForm

register = template.Library()

@register.inclusion_tag('quote/loginForm.html')
def login_form():
    return {'form': LoginForm}
