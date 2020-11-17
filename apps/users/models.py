from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Кастомная модель пользователей"""

    email = models.EmailField(
        ("email address"),
        unique=True,
        error_messages={
            'unique': _("Такой email уже зарегистрирован")
        }
    )
    is_expert = models.BooleanField(
        _("cтатус эксперта"),
        default=False,
        help_text=_("Отметьте, если пользователь является экспертом.")
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    middle_name = models.CharField(
        _('отчество'),
        max_length=150,
        blank=True
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class ExpertsList(models.Model):
    """Модель экспертов"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
