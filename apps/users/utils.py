from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


class UserAuthenticatedMixin:
    @method_decorator(
        user_passes_test(
            lambda u: not u.is_authenticated, login_url="applications_output_url"
        )
    )
    def dispatch(self, *args, **kwargs):
        return super(UserAuthenticatedMixin, self).dispatch(*args, **kwargs)
