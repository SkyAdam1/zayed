from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.views.generic.edit import UpdateView

from apps.users.models import ExpertsList

from . import forms
from .models import Application, ApplicationReport, DesignatedExpert
from .utils import (ObjectDetailMixin, ReportsDetailMixin,
                    UserAuthenticatedMixin)


def index(request):
    return render(request, 'applications/index.html')


def output(request):
    return render(request, 'applications/applications_output.html')


class ApplicationsOutputView(LoginRequiredMixin, View):
    """cписок заявок"""
    def get(self, request):
        application = None
        statuses = []
        if(request.user.is_superuser):
            application = Application.objects.all()
        elif(request.user.is_expert):
            obj = get_object_or_404(ExpertsList, user=request.user)
            apps = DesignatedExpert.objects.filter(expert=obj)
            application = []
            for app in apps:
                application.append(get_object_or_404(Application, pk=app.app.pk))
        elif(request.user.is_active):
            application = Application.objects.filter(user=request.user)
        for item in application:
            statuses.append(item.status)
        return render(request, 'applications/applications_output.html', context={'application': application, 'statuses': statuses})


class ApplicationAddExpert(LoginRequiredMixin, CreateView):
    """добавление эксперта для заявки"""
    model = DesignatedExpert
    form_class = forms.DesignatedExpertForm
    template_name = 'applications/applications_add_expert.html'
    success_url = reverse_lazy('applications_output_url')

    def get(self, request, pk):
        obj = get_object_or_404(Application, pk=pk)
        experts = self.model.objects.filter(app=obj)
        return render(request, self.template_name, context={
            'applications': obj,
            'form': self.form_class,
            'experts': experts})

    def post(self, request, pk):
        obj = get_object_or_404(Application, pk=pk)
        experts = self.model.objects.filter(app=obj)
        if len(experts) < 3:
            for ex in experts:
                if str(ex.expert.id) == request.POST['expert']:
                    return redirect('applications_add_expert_url', pk)
            form = self.form_class(request.POST)
            if form.is_valid():
                exp = form.save(commit=False)
                exp.app = obj
                exp.save()
        return redirect('applications_add_expert_url', pk)


def remove_expert(request, app, user):
    obj = get_object_or_404(DesignatedExpert, app=app, expert=user)
    if request.user.is_staff:
        obj.delete()
    return redirect('applications_add_expert_url', app)


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
        if(request.user.is_superuser):
            application = ApplicationReport.objects.all()
        elif(request.user.is_expert):
            obj = get_object_or_404(ExpertsList, user=request.user)
            apps = DesignatedExpert.objects.filter(expert=obj)
            application = []
            for app in apps:
                a_ = get_object_or_404(Application, pk=app.app.pk)
                application.append(ApplicationReport.objects.get(app=a_.pk))
        elif(request.user.is_active):
            application = ApplicationReport.objects.filter(app__user=request.user)
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
