# logbook/templatetags/logbook_tags.py
from django import template
import re

register = template.Library()

@register.filter
def cut(value, arg):
    """Removes all occurrences of arg from the given string, specifically handling 'page=xyz&' or '&page=xyz'."""
    # Regex to remove 'page=<number>' potentially followed by '&', or preceded by '&'
    page_param_pattern = r'&?page=\d+&?'
    cleaned_value = re.sub(page_param_pattern, '', str(value))
    # If removal left a trailing '&', remove it. Or leading '&' if page was first.
    if cleaned_value.endswith('&'):
        cleaned_value = cleaned_value[:-1]
    if cleaned_value.startswith('&'):
        cleaned_value = cleaned_value[1:]
    return cleaned_value


@register.filter
def add_ampersand(value):
    """Adds an ampersand if the string is not empty."""
    # Simplified: just add & if value exists. Assumes it's appended to '?' or another '&'.
    if value:
        return value + '&'
    return value
