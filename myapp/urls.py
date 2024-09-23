from django.urls import path
from . import views 

urlpatterns = [
    path("", views.dashboard, name="dashboard"),  # Dashboard
    path(
        "scraping/", views.start_scraping_task, name="scraping"
    ),  # Start scraping task
    path(
        "start-task/", views.start_scraping_task, name="start_scraping_task"
    ),  # Start scraping task
    path("analysis/", views.analysis_view, name="analysis"),  # Analysis view
    path("pause-task/<int:task_id>/", views.pause_task, name="pause_task"),
    path("cancel-task/<int:task_id>/", views.cancel_task, name="cancel_task"),
    path("reports/", views.reports_view, name="reports"),  # Reports view
    path(
        "ongoing-tasks/", views.ongoing_scraping_tasks, name="ongoing_scraping_tasks"
    ),  # Ongoing tasks
    path(
        "completed-tasks/",
        views.completed_scraping_tasks,
        name="completed_scraping_tasks",
    ),
    path(
        "completed-tasks/",
        views.completed_scraping_tasks,
        name="completed_scraping_tasks",
    ),  # Completed tasks
    # path("download-data/", views.download_data, name="download_data"),
    path("download-data/<int:task_id>/", views.download_data, name="download_data"),
    path("view-results/<int:task_id>/", views.view_results, name="view_results"),
    path("settings/", views.settings, name="settings"),  # Settings page
    path(
        "save-settings/", views.save_scraping_settings, name="save_scraping_settings"
    ),  # Save settings
    path("start-analysis/", views.start_analysis, name="start_analysis"),
    path("perform-analysis/", views.perform_analysis, name="perform_analysis"),
    path("error/", views.error_page, name="error_page"),
    path("help/", views.help_view, name="help"),  # Help page
    path("profile/", views.profile_view, name="profile"),  # Profile page
    path("logout/", views.logout_view, name="logout"),  # Logout
]
