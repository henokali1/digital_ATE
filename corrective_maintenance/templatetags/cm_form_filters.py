# In your app's templatetags/form_filters.py

from django import template
register = template.Library()

@register.filter(name='addClass')
def cm_my_filter(field, css_class):
    return field.as_widget(attrs={'class': css_class})

@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})
