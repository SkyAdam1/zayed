from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


class UserAuthenticatedMixin:
    @method_decorator(user_passes_test(lambda u: not u.is_authenticated, login_url=reverse_lazy('applications_output_url')))
    def dispatch(self, *args, **kwargs):
        return redirect('applications_output_url')
