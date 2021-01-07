from django.contrib.auth import login, views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, DetailView, View
from django.views.generic.edit import UpdateView

from .forms import (
    CustomUserLoginForm,
    CustomUserRegistrationForm,
    ExpertProfileForm,
    ProfileForm,
)
from .models import CustomUser, ExpertProfile, UserProfile
from .utils import UserAuthenticatedMixin


class UserLoginView(UserAuthenticatedMixin, views.LoginView):
    template_name = "users/login.html"
    form_class = CustomUserLoginForm
    success_url = reverse_lazy("applications_output_url")

    def get_success_url(self):
        return self.success_url


class ExpertLoginView(View):
    template_name = "users/login_expert.html"

    def get(self, request):
        return render(request, self.template_name)


class UserLogoutView(views.LogoutView):
    next_page = reverse_lazy("login_url")


class UserRegistrationView(CreateView):
    model = CustomUser
    template_name = "users/registration.html"
    form_class = CustomUserRegistrationForm
    success_url = reverse_lazy("login_url")
    # success_msg = 'Пользователь успешно создан'

    def form_valid(self, form):
        user = form.save(commit=False)
        if user.is_expert is True:
            user.is_active = False
            user.save()
            return HttpResponseRedirect(reverse_lazy("login_expert_url"))
        user.save()
        # current_site = get_current_site(self.request)
        # mail_subject = 'Активация аккаунта'
        # message = render_to_string('users/user_activate_email.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': PasswordResetTokenGenerator().make_token(user),
        # })
        # to_email = form.cleaned_data.get('email')
        # email = EmailMessage(
        #     mail_subject, message, to=[to_email]
        # )
        # email.send()
        return HttpResponseRedirect(reverse_lazy("login_url"))


class UserActivateView(View):
    template_name = "users/user_activate.html"

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except Exception as e:
            user = None
            print(e)
        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            if user.is_expert:
                return HttpResponse("Ваша заявка была отправлена на рассмотрение.")
            user.is_active = True
            user.save()
            login(request, user)
            return render(request, self.template_name)
        else:
            return HttpResponse("Ссылка на активацию аккаунта недействительна!")


class Experts(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            users = CustomUser.objects.filter(is_expert=True, is_active=False)
            return render(
                request, "users/experts_output.html", context={"experts": users}
            )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class ActiveExpert(View):
    def get(self, request, pk):
        if request.user.is_superuser:
            user = CustomUser.objects.filter(pk=pk).first()
            user.is_active = True
            user.save()
            # current_site = get_current_site(self.request)
            # mail_subject = 'Ваша заявка на статус эксперта была принята'
            # message = render_to_string('users/expert_activate_email.html', {
            #     'user': user,
            #     'domain': current_site,
            # })
            # to_email = user.email
            # email = EmailMessage(
            #     mail_subject, message, to=[to_email]
            # )
            # email.send()
        return HttpResponseRedirect(reverse_lazy("experts"))


class PasswordResetView(views.PasswordResetView):
    template_name = "users/password_reset.html"
    success_url = reverse_lazy("password_reset_done_url")
    email_template_name = "users/password_reset_email.html"


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete_url")


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """ профиль """

    model = UserProfile
    template_name = "users/user_profile_update.html"
    form_class = ProfileForm

    def dispatch(self, *args, **kwargs):
        user = get_object_or_404(self.model, pk=self.kwargs["pk"])
        if self.request.user == user.profile:
            return super(ProfileUpdateView, self).dispatch(*args, **kwargs)
        return HttpResponseRedirect(
            reverse_lazy("user_profile_detail_url", kwargs=self.kwargs)
        )

    def get_success_url(self):
        return reverse_lazy("user_profile_detail_url", kwargs={"pk": self.object.pk})


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """ обзор профиля юзера """

    model = UserProfile
    template_name = "users/user_profile_detail.html"


class ExpertUpdateView(LoginRequiredMixin, UpdateView):
    """ профиль эксперта """

    model = ExpertProfile
    template_name = "users/expert_profile_update.html"
    form_class = ExpertProfileForm

    def dispatch(self, *args, **kwargs):
        user = get_object_or_404(self.model, pk=self.kwargs["pk"])
        if self.request.user == user.profile:
            return super(ExpertUpdateView, self).dispatch(*args, **kwargs)
        return HttpResponseRedirect(
            reverse_lazy("user_profile_detail_url", kwargs=self.kwargs)
        )

    def get_success_url(self):
        return reverse_lazy("expert_profile_detail_url", kwargs={"pk": self.object.pk})


class ExpertProfileDetailView(LoginRequiredMixin, DetailView):
    """ обзор профиля эксперта"""

    model = ExpertProfile
    template_name = "users/expert_profile_detail.html"
