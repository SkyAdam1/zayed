from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index_url"),
    path(
        "application_edit/<slug:pk>",
        views.ApplicationUpdateView.as_view(),
        name="application_update_url",
    ),
    path(
        "applications/",
        views.ApplicationsOutputView.as_view(),
        name="applications_output_url",
    ),
    path(
        "application/<int:pk>/",
        views.ApplicationsOutputView.as_view(),
        name="applications_output_pk_url",
    ),
    path(
        "application_add_expert/<int:pk>/",
        views.ApplicationAddExpert.as_view(),
        name="applications_add_expert_url",
    ),
    path(
        "application_remove_expert/<int:app>/<int:user>/",
        views.remove_expert,
        name="remove_expert_url",
    ),
    path(
        "application_create/",
        views.ApplicationsCreateView.as_view(),
        name="applications_create_url",
    ),
    path(
        "applications_delete/<int:pk>/",
        views.ApplicationDelete.as_view(),
        name="application_delete_url",
    ),
    path(
        "application_detail/<int:id>",
        views.ApplicationsDetailView.as_view(),
        name="applications_detail_url",
    ),
    path(
        "applications_status/<int:id>",
        views.switch_application_status,
        name="switch_status",
    ),
    path(
        "applications_approve/<int:id>",
        views.switch_application_approve,
        name="switch_status_reporta",
    ),
    path(
        "reports/",
        views.ApplicationsReportingView.as_view(),
        name="applications_reporting_url",
    ),
    path(
        "create_report/",
        views.ApplicationReportView.as_view(),
        name="applications_add_report_url",
    ),
    path(
        "report_detail/<int:id>",
        views.ReportsDetail.as_view(),
        name="reports_detail_url",
    ),
    path(
        "report_update/<slug:pk>",
        views.ReportUpdateView.as_view(),
        name="report_update_url",
    ),
    path(
        "report_delete/<int:pk>/",
        views.ReportDelete.as_view(),
        name="report_delete_url",
    ),
    path(
        "report_approve/<int:id>/", views.switch_report_status, name="switch_status_rep"
    ),
    path("report_send/<int:id>/", views.send_report, name="send_report"),
    path("update_remarks/<int:pk>/", views.delete_remarks, name="update_remarks_url"),
    path("delete_comment/<int:pk>/", views.delete_comment, name="delete_comment"),
    path("delete_remark/<int:pk>/", views.delete_remark, name="delete_remark"),
    path("export_xls/", views.export_xls, name="export_xls"),
]
