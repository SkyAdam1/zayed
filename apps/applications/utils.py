from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from apps.applications import forms, models


class ObjectDetailMixin:
    """миксин для обзора заявки"""
    model = models.Application
    form_class = forms.ApplicationCommentForm
    template_name = 'applications/applications_detail.html'

    def get(self, request, id):
        obj = get_object_or_404(self.model, id=id)
        comments = models.ApplicationComment.objects.filter(application=id)
        return render(request, self.template_name, context={
            'applications': obj,
            'form': self.form_class,
            'comments': comments})

    def post(self, request, id):
        obj = get_object_or_404(self.model, id=id)
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.application = obj
            comment.user = request.user
            comment.save()
        return redirect('applications_detail_url', id=id)


class UserAuthenticatedMixin:
    """ограничение доступа для админов и экспертов"""
    @method_decorator(user_passes_test(lambda u: not u.is_staff or not u.is_expert, login_url=reverse_lazy('applications_output_url')))
    def dispatch(self, *args, **kwargs):
        return super(UserAuthenticatedMixin, self).dispatch(*args, **kwargs)


class ReportsDetailMixin:
    """замечания"""
    model = models.ApplicationReport
    form_class = forms.ApplicationRemarkForm
    template_name = 'applications/reports_detail.html'

    def get(self, request, id):
        obj = get_object_or_404(self.model, id=id)
        remarks = models.ApplicationRemark.objects.filter(application=obj)
        return render(request, self.template_name, context={
            'applications': obj,
            'form': self.form_class,
            'remarks': remarks})

    def post(self, request, id):
        obj = get_object_or_404(self.model, id=id)
        form = self.form_class(request.POST)
        if form.is_valid():
            remark = form.save(commit=False)
            remark.application = obj
            remark.user = request.user
            remark.save()
        return redirect('reports_detail_url', id=id)
