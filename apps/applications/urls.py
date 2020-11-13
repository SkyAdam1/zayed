from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index_url'),
    path('applications_output/', views.ApplicationsOutputView.as_view(), name='applications_output_url'),
    path('applications_add_expert/<slug:pk>/', views.ApplicationAddExpert.as_view(), name='applications_add_expert_url'),
    path('applications_create/', views.ApplicationsCreateView.as_view(), name='applications_create_url'),
    path('applications_detail/<int:id>', views.ApplicationsDetailView.as_view(), name='applications_detail_url'),
    path('applications_reporting/', views.ApplicationsReportingView.as_view(), name='applications_reporting_url'),
    path('applications_status/<int:id>', views.switch_application_status, name='switch_status'),
]
