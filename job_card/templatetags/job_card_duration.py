from django import template
from datetime import timedelta

register = template.Library()

@register.filter(name='jobcard_duration')
def job_card_duration(value):
    if isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours:
           return f"{hours} hour{'' if hours == 1 else 's'}, {minutes} minute{'' if minutes == 1 else 's'}, {seconds} second{'' if seconds == 1 else 's'}"
        if minutes:
            return f"{minutes} minute{'' if minutes == 1 else 's'}, {seconds} second{'' if seconds == 1 else 's'}"
        return f"{seconds} second{'' if seconds == 1 else 's'}"
    
    return ''