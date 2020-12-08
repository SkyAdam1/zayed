from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .managers import CustomUserManager
from django.db.models.fields import (BooleanField, CharField, DateField,
                                     DateTimeField, EmailField, IntegerField,
                                     PositiveIntegerField, TextField, URLField)
from django.db.models.deletion import CASCADE
from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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


class UserProfil(models.Model):
    profile = models.OneToOneField(CustomUser ,
        on_delete=CASCADE ,
    )

    phone_number = IntegerField(
        _("Номер телефона для связи")
    )

    mail = CharField(_("Почтовый адрес"),max_length=200, blank=True
    )

    inn = IntegerField(_('Ваш ИНН')
    )

    legal_address = CharField(_('Юридический адрес'),max_length=200, blank=True
    )

    director_fio = CharField(_('ФИО Ген.Директора' ),max_length=200 , blank=True
    )

    rs = IntegerField(_('Расчетный счет')
    )

    bank = CharField(_('Банк'),max_length=200 , blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()