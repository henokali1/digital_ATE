from django import template

register = template.Library()

@register.filter
def count_inspected(inspections):
    """Count inspections that have a non-empty status"""
    return sum(1 for inspection in inspections if inspection.status)

@register.filter
def count_not_inspected(inspections):
    """Count inspections that have an empty status"""
    return sum(1 for inspection in inspections if not inspection.status)