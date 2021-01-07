from django import template
from django.conf import settings

register = template.Library()


@register.filter(name="media_folder_users")
def media_folder_users(string):
    if not string:
        return f"{settings.STATIC_URL}images/user.png"

    return f"{settings.MEDIA_URL}{string}"
