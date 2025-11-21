from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def highlight(value, query):
    """Wrap matching substrings of 'value' with <mark> for the given query.
    Case-insensitive; safely escapes original value and marks result safe.
    """
    if not value or not query:
        return value
    try:
        pattern = re.compile(re.escape(str(query)), re.IGNORECASE)
        escaped = escape(str(value))
        result = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", escaped)
        return mark_safe(result)
    except Exception:
        return value