from django.contrib import admin
from .models import ProjectDetail, ProjectActivitiesDetail, WorkReport


# Register your models here.

@admin.register(ProjectDetail)
class ProjectsAdmin(admin.ModelAdmin):
    list_display =  [field.name for field in ProjectDetail._meta.get_fields()]


@admin.register(ProjectActivitiesDetail)
class ProjectsFeaturesAdmin(admin.ModelAdmin):
    list_display =  [field.name for field in ProjectActivitiesDetail._meta.get_fields()]


@admin.register(WorkReport)
class WorkReportAdmin(admin.ModelAdmin):
    list_display =  [field.name for field in WorkReport._meta.get_fields()]