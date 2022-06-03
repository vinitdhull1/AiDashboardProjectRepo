from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField

# Create your models here.

class ProjectDetail(models.Model):
    proj_name = models.CharField(max_length=500)
    proj_status = models.CharField(max_length=500, blank=True)
    proj_starting_date = models.CharField(max_length=500, blank=True)
    proj_last_updated = models.CharField(max_length=500, blank=True)
    proj_bussiness_person_involved = models.CharField(max_length=500, blank=True)
    proj_developers_involved = models.CharField(max_length=500, blank=True)
    proj_url = models.CharField(max_length=500, blank=True)
    proj_remarks = models.CharField(max_length=500, blank=True)

class ProjectActivitiesDetail(models.Model):
    proj_name = models.CharField(max_length=500)
    activities = models.CharField(max_length=500, blank=True)
    activity_start_date = models.CharField(max_length=500, blank=True)
    activity_end_date = models.CharField(max_length=500, blank=True)
    working_days = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=500, blank=True)
    

class WorkReport(models.Model):
    emp_code = models.CharField(max_length=500, blank=True)
    resource_name = models.CharField(max_length=500, blank=True)
    skill = models.CharField(max_length=500, blank=True)
    actual_hours = models.CharField(max_length=500, blank=True)
    date = models.CharField(max_length=500, blank=True)
    work_details = models.CharField(max_length=500, blank=True)
    remark = models.CharField(max_length=500, blank=True)
    clients = models.CharField(max_length=500, blank=True)