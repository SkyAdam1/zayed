from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserLoginView.as_view(), name=''),
    path('experts/', views.Experts.as_view(), name='experts'),
    path('expert/<int:pk>', views.ActiveExpert.as_view(), name='active_expert'),
    path('login/', views.UserLoginView.as_view(), name='login_url'),
    path('logout/', views.UserLogoutView.as_view(), name='logout_url'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration_url'),
    path('activate/<uidb64>/<token>/', views.UserActivateView.as_view(), name='activate_url'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset_url'),
    path("password_reset_done/", views.PasswordResetDoneView.as_view(), name="password_reset_done_url"),
    path("password_reset_confirm/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm_url"),
    path("password_reset_complete/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete_url"),
    path('user_profile/<int:pk>/', views.ProfileView.as_view(), name='profile_url'),
    path('expert_profile/<int:pk>/', views.ExpertProfileView.as_view(), name='expert_profile_url'),
    path('profile_detail/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail_url'),
]
