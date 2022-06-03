from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('login/', views.log_in, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name="logout"),
    path('project-detail/', views.project_detail, name="project-detail"),
    path('upload-projects/', views.upload_projects, name='upload-projects'),
    path('create-report/', views.create_report, name='create-report'),
    path('edit-projects/<int:id>', views.edit_projects, name='edit-projects'),
    path('edit-project-details/<int:id>', views.edit_project_details, name='edit-project-details'),
    path('edit-work-report/<int:id>', views.edit_work_report, name='edit-work-report'),
    path('delete-report/<int:id>', views.delete_report, name='delete-report'),
    path('delete-project/<int:id>', views.delete_project, name='delete-project'),
    path('delete-project-feature/<int:id>', views.delete_project_feature, name='delete-project-feature'),
    path('download-excel-data/', views.download_excel_data, name='download-excel-data')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
