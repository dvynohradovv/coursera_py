from django import template

register = template.Library()


@register.filter
def inc(value, add_arg):
    return int(float(value)) + int(float(add_arg))


@register.simple_tag
def division(divisible, divisor, to_int=True):
    result = float(divisible) / float(divisor)
    return int(result) if to_int else result
