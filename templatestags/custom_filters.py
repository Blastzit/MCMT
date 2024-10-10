from django import template

register = template.Library()

@register.filter
def sentence_break(value):
    return value.replace('. ', '.<br>')