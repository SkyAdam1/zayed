from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import BooleanField, CharField, EmailField
from django.db.models.fields.related import OneToOneField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Кастомная модель пользователей"""

    email = EmailField(
        ("email address"),
        unique=True,
        error_messages={
            'unique': _("Такой email уже зарегистрирован")
        }
    )
    is_expert = BooleanField(
        _("cтатус эксперта"),
        default=False,
        help_text=_("Отметьте, если пользователь является экспертом.")
    )
    is_active = BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    middle_name = CharField(
        _('отчество'),
        max_length=150,
        blank=True
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    photo = models.ImageField(_('Фото профиля'),upload_to='avatar_photos/' , null=True , blank = True ,default='media/files/1.jpg')
    profile = OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = CharField(_("Номер телефона для связи"), blank = True , null=True, max_length=200)
    mail = CharField(_("Почтовый адрес"), max_length=200, blank = True , null=True,)
    inn = CharField(_('Ваш ИНН'), blank = True , null=True, max_length=200)
    ogrn = CharField(_('ОГРН'), blank = True , null=True, max_length=200 )
    legal_address = CharField(_('Юридический адрес'), max_length=200, blank = True , null=True,)
    director_fio = CharField(_('ФИО Ген.Директора'), max_length=200, blank = True , null=True,)
    rs = CharField(_('Расчетный счет'), blank = True , null=True, max_length=200)
    bank = CharField(_('Банк'), max_length=200,  blank = True , null=True)

    def __str__(self):
        return self.profile.username

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created and not instance.is_expert:
            UserProfile.objects.create(profile=instance)

    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        if not instance.is_expert:
            instance.userprofile.save()


class ExpertProfile(models.Model):
    photo = models.ImageField(_('Фото профиля'),upload_to='avatar_photos/' , null=True , blank = True ,default='media/files/1.jpg')
    profile = OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = CharField(_("Номер телефона для связи"), blank = True , null=True, max_length=200)
    work_place = CharField(_('Место работы'), blank = True , null=True, max_length=200)
    position = CharField(_('Занимаемая должность'), blank = True , null=True, max_length=200)
    interests = CharField(_('Сфера профессиональных интересов'), blank = True , null=True, max_length=200)
    edu = [
        ('Высшее', 'Высшее'),
        ('Среднее профессиональное', 'Среднее профессиональное'),
    ]
    education = CharField(_('Образование'), choices=edu, blank=True, null=True, max_length=200)
    degree = CharField(_('Степень образования'), blank = True , null=True, max_length=200)

    def __str__(self):
        return self.profile.username

    @receiver(post_save, sender=CustomUser)
    def create_expert_profile(sender, instance, created, **kwargs):
        if created and instance.is_expert:
            ExpertProfile.objects.create(profile=instance)

    @receiver(post_save, sender=CustomUser)
    def save_expert_profile(sender, instance, **kwargs):
        if instance.is_expert:
            instance.expertprofile.save()
