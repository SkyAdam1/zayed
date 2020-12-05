from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.views.generic.edit import DeleteView, UpdateView

from . import forms
from .models import (Application, ApplicationRemark, ApplicationReport,
                     DesignatedExpert, ApplicationComment)
from .utils import (ObjectDetailMixin, ReportsDetailMixin,
                    UserAuthenticatedMixin)



def delete_remarks(request, pk):
    obj = get_object_or_404(ApplicationReport, app=pk)
    remarks = ApplicationRemark.objects.filter(application=obj)
    remarks.delete()
    return HttpResponseRedirect(reverse_lazy('applications_reporting_url'))
