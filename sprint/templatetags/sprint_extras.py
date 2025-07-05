from django import template

register = template.Library()

@register.filter
def format_duration(td):
    if td is None:
        return "0 seconds"
    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{days} days {hours} hrs {minutes} mins {seconds} seconds"
