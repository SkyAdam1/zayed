from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import (BooleanField, CharField, DateField,
                                     DateTimeField, EmailField, IntegerField,
                                     PositiveIntegerField, TextField, URLField)
from django.db.models.fields.files import FileField
from django.db.models.fields.related import ForeignKey
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from apps.users.models import ExpertsList

from .validators import validate_file_extension


class Application(models.Model):
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE)

    data_create = DateTimeField(
        _("Время создания"),
        auto_now_add=True)

    project_name = CharField(
        _("Название проекта"),
        max_length=150,
        db_index=True)

    project_site = URLField(
        _("Ссылка на официальный сайт проекта"),
        max_length=200)

    data_project_start = DateField(
        _("Дата начала работы на проектом"))

    legal_entity = BooleanField(
        _("Юридическое лицо"),
        default=False)

    project_stage = CharField(
        _("На какой стадии развития находится ваш проект?"),
        max_length=150)

    project_description = TextField(
        _("Описание продукта/сервиса"))

    businessmodel_description = TextField(
        _("Описание бизнес-модели"))

    problem_decision = TextField(
        _("Какую проблему решает ваш продукт/сервис?"))

    consumer_decision = TextField(
        _("Как на данный момент потребители решают данную проблему?"))

    product_difference = TextField(
        _("Чем Ваш продукт / сервис отличается от текущего способа решения проблемы?"))

    have_photo = BooleanField(
        _("Есть ли фото/видео проекта?"),
        default=False)

    photo_video_project = URLField(
        _("Ссылка на фото/видео продукта"),
        max_length=200,
        blank=True)

    patentability = CharField(
        _("Насколько проработана патентоспособность продукта/услуги?"),
        max_length=150)

    market_size = CharField(
        _("Оцените объем Вашего рынка?"),
        max_length=150)

    marketing_description = TextField(
        _("Описание маркетинговой стратегии"))

    sale_strategy = TextField(
        _("Описание стратегии продаж"))

    desciption_risk = TextField(
        _("Описание существующих рисков"))

    client_count = IntegerField(
        _("Количество клиентов на данный момент"))

    previous_investors = CharField(
        _("Предыдущие инвесторы (ФИО, сумма инвестиций)"),
        max_length=500)

    middle_cost = CharField(
        _("Какая среднегодовая сумма издержек у вашей компании / проекта за последние 2 года"),
        max_length=50)

    budget_development = CharField(
        _("Какая сумма инвестирования вам необходима для дальнейшего развития?"),
        max_length=50)

    middle_revenue = CharField(
        _("Какая среднегодовая сумма выручки у вашей компании / проекта за последние 2 года?"),
        max_length=50)

    team_count = IntegerField(
        _("Количество человек в команде"))

    fio_team = TextField(
        _("ФИО членов команды"))

    team_education = CharField(
        _("Полученное образование членов команды"),
        max_length=500)

    team_experience = CharField(
        _("Опыт работы членов команды"),
        max_length=500)
    position_member = TextField(
        _("Текущая занимаемая должность членов команды"))

    residence_member = CharField(
        _("Текущее место жительства членов команды"),
        max_length=500)

    team_create = CharField(
        _("Как вы познакомились и пришли к решению работать вместе?"),
        max_length=2000)

    ready_relocate = BooleanField(
        _("Готова ли ваша команда переехать на время акселерационной программы в г.Грозный Чеченская Республика?"))

    ready_development = BooleanField(
        _("Готова ли ваша команда посвятить все свое время развитию проекта в соответствии с акселерационной программой?"))

    adress_company = CharField(
        _("Адрес компании"),
        max_length=150)

    inn_company = CharField(
        _("ИНН компании"),
        max_length=12)

    fio = CharField(
        _("ФИО контактного лица"),
        max_length=150,
        db_index=True)

    email = EmailField(
        _("Почта контактного лица"),
        max_length=254)

    status = BooleanField(
        _("Статус заявки"),
        default=False)
    approved = BooleanField(
        _("Одобрено/Не добрено"),
        default=False)
    upload = FileField(
        upload_to='files/', null=True, blank=True)

    def get_update_url(self):
        return reverse('application_update_url', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('applications_detail_url', kwargs={'id': self.id})

    def __str__(self) -> str:
        return self.project_name


class DesignatedExpert(models.Model):
    rate = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    app = ForeignKey(Application, CASCADE)
    expert = ForeignKey(ExpertsList, CASCADE, verbose_name='Эксперт')
    rating = PositiveIntegerField(_('Оценка'), choices=rate, blank=True, null=True)

    def __str__(self):
        return f'{self.app}: {self.expert} - {self.rating}'


class ApplicationComment(models.Model):
    application = ForeignKey(
        Application,
        on_delete=CASCADE)
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE)
    text = TextField(
        _('Текст комментария'))
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return 'Комментарий {} от {}'.format(self.text, self.user.username)


class ApplicationReport(models.Model):
    app = ForeignKey(
        Application,
        on_delete=CASCADE,
        default=None,
        verbose_name='Заявка')

    upload = FileField(
        upload_to='reporting/', null=True,
        validators=[validate_file_extension])

    status_reporta = BooleanField(
        _("Статус отчетности"),
        default=False)

    def __str__(self):
        return self.app.project_name


class ApplicationRemark(models.Model):
    application = ForeignKey(
        ApplicationReport,
        on_delete=CASCADE)
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE)
    text = TextField(
        _('Текст замечания'))
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return 'Замечание {} от {}'.format(self.text, self.user.username)
