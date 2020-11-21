from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.views.generic.edit import UpdateView
from .utils import UserAuthenticatedMixin, ObjectDetailMixin, ReportsDetailMixin
from . import forms
from .models import Application, ApplicationReport


def index(request):
    return render(request, 'applications/index.html')


def output(request):
    return render(request, 'applications/applications_output.html')


class ApplicationsOutputView(LoginRequiredMixin, View):
    """писок заявок"""
    def get(self, request):
        application = None
        statuses = []
        if(request.user.is_superuser or request.user.is_expert):
            application = Application.objects.all()
        elif(request.user.is_active):
            application = Application.objects.filter(user=request.user)
        for item in application:
            statuses.append(item.status)
        return render(request, 'applications/applications_output.html', context={'application': application, 'statuses': statuses})


class ApplicationAddExpert(LoginRequiredMixin, UpdateView):
    """добавление эксперта для заявки"""
    model = Application
    fields = ['designated_expert']
    template_name = 'applications/applications_add_expert.html'
    login_url = reverse_lazy('login_url')
    success_url = reverse_lazy('applications_output_url')


class ApplicationsCreateView(UserAuthenticatedMixin,  LoginRequiredMixin, CreateView):
    """создание заявки"""
    model = Application
    template_name = 'applications/applications_create.html'
    form_class = forms.ApplicationCreateForm
    success_url = reverse_lazy('applications_output_url')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ApplicationsDetailView(LoginRequiredMixin, ObjectDetailMixin, View):
    """обзор заявки"""
    model = Application
    template_name = 'applications/applications_detail.html'
    form_class = forms.ApplicationCommentForm
    success_url = reverse_lazy('applications_detail_url')


class ApplicationsReportingView(LoginRequiredMixin, View):
    """список отчетов"""
    def get(self, request):
        application = None
        if(request.user.is_superuser or request.user.is_expert):
            application = ApplicationReport.objects.all()
        elif(request.user.is_active):
            application = ApplicationReport.objects.filter()
        return render(request, 'applications/applications_reporting.html', context={'application': application})


def switch_application_status(request, id):
    """одобрение или отклонение заявки"""
    app = get_object_or_404(Application, pk=id)
    if app.user == request.user or request.user.is_staff:
        if app.status:
            app.status = False
            app.save()
        else:
            app.status = True
            app.save()
    return HttpResponseRedirect(reverse_lazy('applications_output_url'))


class ApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """редактирование заявки"""
    model = Application
    fields = [
        'project_name', 'project_site', 'data_project_start', 'legal_entity',
        'project_stage', 'project_description', 'businessmodel_description', 'problem_decision',
        'consumer_decision', 'product_difference', 'have_photo', 'photo_video_project', 'patentability',
        'market_size', 'marketing_description', 'sale_strategy', 'desciption_risk', 'client_count',
        'previous_investors', 'middle_cost', 'budget_development', 'middle_revenue', 'team_count',
        'fio_team', 'team_education', 'team_experience', 'position_member', 'team_create', 'ready_relocate',
        'ready_development', 'adress_company', 'inn_company', 'fio', 'email', 'upload']
    template_name = 'applications/application_update_form.html'
    success_url = reverse_lazy('applications_output_url')


class ApplicationReportView(UserAuthenticatedMixin, LoginRequiredMixin, CreateView):
    """Добавление отчетности"""
    model = ApplicationReport
    template_name = 'applications/applications_add_report.html'
    login_url = reverse_lazy('login_url')
    success_url = reverse_lazy('applications_output_url')
    form_class = forms.ApplicationReportForm


class ReportsDetail(LoginRequiredMixin, ReportsDetailMixin, View):
    model = ApplicationReport
    template_name = 'applications/reports_detail.html'
    form_class = forms.ApplicationRemarkForm
    success_url = reverse_lazy('applications_output_url')
