from django.template.defaulttags import register


@register.filter
def get_range(value):
    return range(value)
