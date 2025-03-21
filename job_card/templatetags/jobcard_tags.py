from django import template
from urllib.parse import urlencode

register = template.Library()

@register.filter
def exclude_param(request_get, param_to_exclude):
    """
    Excludes a specific parameter from the request's GET parameters,
    preserving all other parameters.
    """
    get_copy = request_get.copy()
    get_copy.pop(param_to_exclude, None)  # Remove the parameter
    return get_copy