from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import reverse
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


class UserAuthenticatedMixin:
    @method_decorator(user_passes_test(lambda u: not u.is_authenticated, login_url=reverse('applications_output_url')))
    def dispatch(self, *args, **kwargs):
        return super(UserAuthenticatedMixin, self).dispatch(*args, **kwargs)
