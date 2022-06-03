from django import forms
from django.forms import fields
from .models import ProjectDetail, ProjectActivitiesDetail, WorkReport


# Create your forms here.
class ProjectDetailForm(forms.ModelForm):

    class Meta:
        model = ProjectDetail
        fields = ('proj_name', 'proj_status', 'proj_starting_date',
                  'proj_last_updated', 'proj_bussiness_person_involved',
                  'proj_developers_involved', 'proj_url', 'proj_remarks')


class ProjectActivitiesDetailForm(forms.ModelForm):

    class Meta:
        model = ProjectActivitiesDetail
        fields = ('proj_name', 'activities', 'activity_start_date',
                  'activity_end_date', 'working_days', 'status')


class WorkReportForm(forms.ModelForm):

    class Meta:
        model = WorkReport
        fields = ('emp_code', 'resource_name', 'skill', 'actual_hours', 'date',
                  'work_details', 'remark', 'clients')
