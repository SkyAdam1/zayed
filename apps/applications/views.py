from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.views.generic.edit import UpdateView, DeleteView

from . import forms
from .models import (Application, ApplicationRemark, ApplicationReport,
                     DesignatedExpert)
from .utils import (ObjectDetailMixin, ReportsDetailMixin,
                    UserAuthenticatedMixin)


def index(request):
    return render(request, 'applications/index.html')


def output(request):
    return render(request, 'applications/applications_output.html')


class ApplicationsOutputView(LoginRequiredMixin, View):
    """cписок заявок"""
    def get(self, request, pk=None):
        application = None
        statuses = []
        if(request.user.is_superuser):
            application = Application.objects.all()
        elif(request.user.is_expert):
            apps = DesignatedExpert.objects.filter(expert=request.user)
            form = forms.RatingForm
            application = []
            for app in apps:
                _a = get_object_or_404(Application, pk=app.app.pk)
                _a.form = form
                application.append(_a)
        elif(request.user.is_active):
            application = Application.objects.filter(user=request.user)
        for item in application:
            ex = DesignatedExpert.objects.filter(app=item.pk)
            item.experts = ex
            item.rating = 0
            i = 0
            for el in ex:
                if type(el.rating) == int:
                    item.rating += el.rating
                    i += 1
            if i > 0:
                item.rating = item.rating / i
            statuses.append(item.status)
        return render(request, 'applications/applications_output.html', context={'application': application, 'statuses': statuses})

    def post(self, request, pk):
        obj = get_object_or_404(DesignatedExpert, app=pk, expert=request.user.pk)
        obj.rating = request.POST['rating']
        obj.save()
        return redirect('applications_output_url')


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


class ApplicationsCreateView(LoginRequiredMixin, UserAuthenticatedMixin, CreateView):
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
            apps = DesignatedExpert.objects.filter(expert=request.user)
            application = []
            for app in apps:
                try:
                    a_ = get_object_or_404(Application, pk=app.app.pk)
                    application.append(ApplicationReport.objects.get(app=a_.pk))
                except Exception as e:
                    print(e)
        elif(request.user.is_active):
            application = ApplicationReport.objects.filter(app__user=request.user)
        for app in application:
            notifications = len(ApplicationRemark.objects.filter(application=app.id))
            app.notifications = notifications
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


class ApplicationUpdateView(LoginRequiredMixin, UpdateView, UserAuthenticatedMixin):
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


class ApplicationReportView(LoginRequiredMixin, UserAuthenticatedMixin, CreateView):
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


def switch_report_status(request, id):
    report = get_object_or_404(ApplicationReport, pk=id)
    if report.user == request.user or request.user.is_staff:
        if report.status_reporta:
            report.status_reporta = False
            report.save()
        else:
            report.status_reporta = True
            report.save()
    return HttpResponseRedirect(reverse_lazy('applications_reporting_url'))


def switch_application_status_final(request, id):
    """одобрение или отклонение заявки прям до конца"""
    app = get_object_or_404(Application, pk=id)
    if request.user.is_staff:
        if app.approved:
            app.approved = False
            app.status = False
            app.save()
        else:
            app.approved = True
            app.save()
    return HttpResponseRedirect(reverse_lazy('applications_output_url'))


class ReportUpdateView(LoginRequiredMixin, UpdateView, UserAuthenticatedMixin):
    """редактирование отчета"""
    model = ApplicationReport
    fields = ['upload']
    template_name = 'applications/report_update_form.html'
    success_url = reverse_lazy('applications_reporting_url')


class ApplicationDelete(DeleteView, UserAuthenticatedMixin, LoginRequiredMixin):
    ''' удаление заявки '''
    model = Application
    success_url = reverse_lazy('applications_output_url')
    template_name = 'applications/application_delete.html'


class ReportDelete(DeleteView, UserAuthenticatedMixin,  LoginRequiredMixin):
    ''' удаление отчета '''
    model = ApplicationReport
    success_url = reverse_lazy('applications_reporting_url')
    template_name = 'applications/report_delete.html'
