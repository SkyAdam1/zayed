from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from .validators import validate_file_extension


class Application(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    data_create = models.DateTimeField(
        _("Время создания"),
        auto_now_add=True)

    project_name = models.CharField(
        _("Название проекта"),
        max_length=150,
        db_index=True)

    project_site = models.URLField(
        _("Ссылка на официальный сайт проекта"),
        max_length=200)

    data_project_start = models.DateField(
        _("Дата начала работы на проектом"))

    legal_entity = models.BooleanField(
        _("Юридическое лицо"),
        default=False)

    project_stage = models.CharField(
        _("На какой стадии развития находится ваш проект?"),
        max_length=150)

    project_description = models.TextField(
        _("Описание продукта/сервиса"))

    businessmodel_description = models.TextField(
        _("Описание бизнес-модели"))

    problem_decision = models.TextField(
        _("Какую проблему решает ваш продукт/сервис?"))

    consumer_decision = models.TextField(
        _("Как на данный момент потребители решают данную проблему?"))

    product_difference = models.TextField(
        _("Чем Ваш продукт / сервис отличается от текущего способа решения проблемы?"))

    have_photo = models.BooleanField(
        _("Есть ли фото/видео проекта?"),
        default=False)

    photo_video_project = models.URLField(
        _("Ссылка на фото/видео продукта"),
        max_length=200,
        blank=True)

    patentability = models.CharField(
        _("Насколько проработана патентоспособность продукта/услуги?"),
        max_length=150)

    market_size = models.CharField(
        _("Оцените объем Вашего рынка?"),
        max_length=150)

    marketing_description = models.TextField(
        _("Описание маркетинговой стратегии"))

    sale_strategy = models.TextField(
        _("Описание стратегии продаж"))

    desciption_risk = models.TextField(
        _("Описание существующих рисков"))

    client_count = models.IntegerField(
        _("Количество клиентов на данный момент"))

    previous_investors = models.CharField(
        _("Предыдущие инвесторы (ФИО, сумма инвестиций)"),
        max_length=500)

    middle_cost = models.CharField(
        _("Какая среднегодовая сумма издержек у вашей компании / проекта за последние 2 года"),
        max_length=50)

    budget_development = models.CharField(
        _("Какая сумма инвестирования вам необходима для дальнейшего развития?"),
        max_length=50)

    middle_revenue = models.CharField(
        _("Какая среднегодовая сумма выручки у вашей компании / проекта за последние 2 года?"),
        max_length=50)

    team_count = models.IntegerField(
        _("Количество человек в команде"))

    fio_team = models.TextField(
        _("ФИО членов команды"))

    team_education = models.CharField(
        _("Полученное образование членов команды"),
        max_length=500)

    team_experience = models.CharField(
        _("Опыт работы членов команды"),
        max_length=500)
    position_member = models.TextField(
        _("Текущая занимаемая должность членов команды"))

    residence_member = models.CharField(
        _("Текущее место жительства членов команды"),
        max_length=500)

    team_create = models.CharField(
        _("Как вы познакомились и пришли к решению работать вместе?"),
        max_length=2000)

    ready_relocate = models.BooleanField(
        _("Готова ли ваша команда переехать на время акселерационной программы в г.Грозный Чеченская Республика?"))

    ready_development = models.BooleanField(
        _("Готова ли ваша команда посвятить все свое время развитию проекта в соответствии с акселерационной программой?"))

    adress_company = models.CharField(
        _("Адрес компании"),
        max_length=150)

    inn_company = models.CharField(
        _("ИНН компании"),
        max_length=12)

    fio = models.CharField(
        _("ФИО контактного лица"),
        max_length=150,
        db_index=True)

    email = models.EmailField(
        _("Почта контактного лица"),
        max_length=254)

    status = models.BooleanField(
        _("Статус заявки"),
        default=False)

    upload = models.FileField(
        upload_to='files/', null=True, blank=True,
        validators=[validate_file_extension])

    def get_update_url(self):
         return reverse('application_update_url' , kwargs =  {'pk' : self.pk})

    designated_expert = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        default=None,
        null=True,
        related_name='Expert')

    def get_absolute_url(self):
        return reverse('applications_detail_url', kwargs={'id': self.id})

    def __str__(self) -> str:
        return self.project_name


class ApplicationComment(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    text = models.TextField(
        _('Текст комментария'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return 'Комментарий {} от {}'.format(self.text, self.user.username)
