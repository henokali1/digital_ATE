# In your app's templatetags/form_filters.py

from django import template
register = template.Library()

@register.filter(name='addClass')
def cm_my_filter(field, css_class):
    return field.as_widget(attrs={'class': css_class})
