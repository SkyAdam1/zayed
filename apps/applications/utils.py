from django.shortcuts import get_object_or_404, redirect, render

from apps.applications import forms
from apps.applications import models


class ObjectDetailMixin:
    model = models.Applications
    form_class = forms.ApplicationsCreateForm
    template_name = 'applications/applications_detail.html'

    def get(self, request, id):
        obj = get_object_or_404(self.model, id=id)
        comments = models.ApplicationsComments.objects.filter(applications=id)
        return render(request, self.template_name, context={
            self.model.__name__.lower(): obj,
            'form': self.form_class,
            'comments': comments})

    def post(self, request, id):
        obj = get_object_or_404(self.model, id=id)
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.applications = obj
            comment.user = request.user
            comment.save()
        return redirect('applications_detail_url', id=id)