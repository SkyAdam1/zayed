from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View

from . import forms, utils
from .models import Applications


def index(request):
    return render(request, 'applications/index.html')


def output(request):
    return render(request, 'applications/applications_output.html')


class ApplicationsOutputView(View):
    def get(self, request):
        application = None
        if(request.user.is_authenticated):
            if(request.user.is_superuser or request.user.is_expert):
                application = Applications.objects.all()
            elif(request.user.is_active):
                application = Applications.objects.filter(user=request.user)
            return render(request, 'applications/applications_output.html', context={'application': application})
        return HttpResponse('Войдите в учетную запись')


class ApplicationsCreateView(CreateView):
    model = Applications
    template_name = 'applications/applications_create.html'
    form_class = forms.ApplicationsCreateForm
    success_url = reverse_lazy('applications_output_url')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ApplicationsDetailView(utils.ObjectDetailMixin, View):
    model = Applications
    template_name = 'applications/applications_detail.html'
    form_class = forms.ApplicationsCreateComment
    success_url = reverse_lazy('applications_detail_url')


class ApplicationsReportingView(View):
    def get(self, request):
        application = None
        if(request.user.is_authenticated):
            if(request.user.is_superuser or request.user.is_expert):
                application = Applications.objects.all()
            elif(request.user.is_active):
                application = Applications.objects.filter(user=request.user)
            return render(request, 'applications/applications_reporting.html', context={'application': application})
        return HttpResponse('Войдите в учетную запись')


def switch_application_status(request, id):
    app = get_object_or_404(Applications, pk=id)
    if app.status:
        app.status = False
        app.save()
    else:
        app.status = True
        app.save()
    return HttpResponseRedirect(reverse_lazy('applications_output_url'))
