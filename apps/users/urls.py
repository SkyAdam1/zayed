from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserLoginView.as_view(), name=''),
    path('experts/', views.Experts.as_view(), name='experts'),
    path('expert/<int:pk>', views.ActiveExpert.as_view(), name='active_expert'),
    path('login/', views.UserLoginView.as_view(), name='login_url'),
    path('login_expert/', views.ExpertLoginView.as_view(), name='login_expert_url'),
    path('logout/', views.UserLogoutView.as_view(), name='logout_url'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration_url'),
    path('activate/<uidb64>/<token>/', views.UserActivateView.as_view(), name='activate_url'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset_url'),
    path('password_reset_done/', views.PasswordResetDoneView.as_view(), name='password_reset_done_url'),
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm_url'),
    path('password_reset_complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete_url'),
    path('user/<int:pk>/', views.ProfileDetailView.as_view(), name='user_profile_detail_url'),
    path('edit_user/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_update_url'),
    path('expert/<int:pk>/', views.ExpertProfileDetailView.as_view(), name='expert_profile_detail_url'),
    path('edit_expert/<int:pk>/', views.ExpertUpdateView.as_view(), name='expert_profile_update_url'),
]
