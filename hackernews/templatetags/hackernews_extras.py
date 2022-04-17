from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter(name='next')
def next(value, arg):
    try:
        return value[int(arg)+1]
    except:
        return None

@register.filter(name='prev')
def prev(value, arg):
    try:
        return value[int(arg)-1]
    except:
        return None

        
@register.filter(name='yesterday')
def yesterday():
    print((datetime.now() - timedelta(1)).strftime('%Y-%m-%d'))
    return (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    
@register.simple_tag(name="yesterday")
def current_time():
    return (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")

register.filter(next)
register.filter(prev)
register.filter(yesterday)
register.tag(current_time)