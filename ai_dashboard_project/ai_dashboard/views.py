from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
from .models import ProjectDetail, ProjectActivitiesDetail, WorkReport
from .forms import ProjectDetailForm, ProjectActivitiesDetailForm, WorkReportForm
from django.shortcuts import get_object_or_404
import xlwt
from django.http import HttpResponse


# Create your views here.
@login_required(login_url='/login/')
def projects(request):
    project_detail = ProjectDetail.objects.all()
    proj_feature = ProjectActivitiesDetail.objects.all()
    if request.method == "POST":
        proj_form = ProjectDetailForm(request.POST)
        if proj_form.is_valid():
            proj_form.save()
            messages.success(request, ('Your project was successfully added!'))
        else:
            messages.error(request, 'Error saving form')
    context = {"proj_detail": project_detail, "proj_feature": proj_feature}
    return render(request, 'projects.html', context)


def log_in(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # return render(request, 'index.html')
            return redirect(projects)
        else:
            messages.error(request, "Invalid Credentials!!!!")
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html', context)


@login_required(login_url='/login/')
def dashboard(request):
    reports = WorkReport.objects.all()
    context = {'reports': reports}
    return render(request, 'dashboard.html', context)


@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return redirect(log_in)


@login_required(login_url='/login/')
def project_detail(request):
    context = {}
    if request.method == "POST" and request.POST.get(
            "proj_query") == "proj_query":
        name = request.POST.get("proj_name")
        proj_activities = ProjectActivitiesDetail.objects.filter(proj_name=name)
        context = {"proj_name": name, "proj_activities": proj_activities}
        return render(request, 'project_detail.html', context)
    if request.method == "POST" and not request.POST.get("proj_query"):
        name = request.POST.get("proj_name")
        feature_form = ProjectActivitiesDetailForm(request.POST)
        if feature_form.is_valid():
            feature_form.save()
            proj_activities = ProjectActivitiesDetail.objects.filter(
                proj_name=name)
            messages.success(request, ('Your feature was successfully added!'))
        else:
            messages.error(request, 'Error saving form')

        context = {"proj_name": name, "proj_activities": proj_activities}
        return render(request, 'project_detail.html', context)
    return render(request, 'project_detail.html', context)


@login_required(login_url='/login/')
def upload_projects(request):
    context = {}
    if request.method == 'POST' and request.FILES:
        try:
            excel_file = request.FILES["project_file"]
        except Exception as err:
            messages.error(request, str(err))
            return redirect(project_detail)

        if (str(excel_file).split('.')[-1] == "xls"):
            data = xls_get(excel_file, column_limit=8)
        elif (str(excel_file).split('.')[-1] == "xlsx"):
            data = xlsx_get(excel_file, column_limit=8)
        else:
            messages.error(request, "Sorry there some problem with your file!")
            return redirect(project_detail)
        if "Project Page" in data:
            project_page = data["Project Page"]
            # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            # print("Project List----->", project_page))
            # print("=======================================================")
            if len(project_page) > 1:
                for project in project_page:
                    if len(project) > 0:  # The row is not blank
                        if project[0] != "Project Name":
                            ProjectDetail.objects.create(
                                proj_name=project[0],
                                proj_status=project[1],
                                proj_starting_date=project[2],
                                proj_last_updated=project[3],
                                proj_bussiness_person_involved=project[4],
                                proj_developers_involved=project[5],
                                proj_url=project[6],
                                proj_remarks=project[7])
        if "Feature Page" in data:
            feature_page = data["Feature Page"]
            project_name = request.POST.get("project_name")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("Project Features List----->", feature_page)
            print("=======================================================")
            if len(feature_page) > 1:
                for feature in feature_page:
                    if len(feature) > 0:
                        if feature[0] != "Features":
                            ProjectActivitiesDetail.objects.create(
                                proj_name=project_name,
                                activities=feature[0],
                                activity_start_date=feature[1],
                                activity_end_date=feature[2],
                                working_days=feature[3],
                                status=feature[4],
                            )
                messages.success(
                    request, "You have successfully added new features for " +
                    project_name + "!")
                proj_feature = ProjectActivitiesDetail.objects.filter(
                    proj_name=project_name)
                context = {
                    "proj_name": project_name,
                    "proj_feature": proj_feature
                }
                return render(request, 'project_detail.html', context)
        messages.success(request, "You have successfully added new projects!")
        return redirect(projects)
    return redirect(projects)


@login_required(login_url='/login/')
def create_report(request):
    if request.method == 'POST' and request.FILES:
        try:
            excel_file = request.FILES["report_file"]
        except Exception as err:
            messages.error(request, str(err))
            return redirect(dashboard)

        if (str(excel_file).split('.')[-1] == "xls"):
            data = xls_get(excel_file, column_limit=9)
        elif (str(excel_file).split('.')[-1] == "xlsx"):
            data = xlsx_get(excel_file, column_limit=9)
        else:
            messages.error(request, "Sorry there some problem with your file!")
            return redirect(dashboard)

        if "AIML" in data:
            report_page = data["AIML"]
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("Work Report Page----->", report_page)
            print("=======================================================")
            if len(report_page) > 1:
                for report in report_page:
                    if len(report) > 0:
                        if report[0] != "Sr,no" and report[
                                0] != "Sr.no" and report[0] != "Sr.No":
                            try:
                                WorkReport.objects.create(
                                    emp_code=report[1],
                                    resource_name=report[2],
                                    skill=report[3],
                                    actual_hours=report[4],
                                    date=report[5],
                                    work_details=report[6],
                                    remark=report[7],
                                    clients=report[8],
                                )
                            except Exception as Err:
                                messages.error(request, Err)
                                return redirect(dashboard)
        return redirect(dashboard)
    if request.method == "POST" and not request.FILES:
        work_report_form = WorkReportForm(request.POST)
        if work_report_form.is_valid():
            work_report_form.save()
            messages.success(request,
                             ('Your work report was successfully created!'))
        else:
            messages.error(request, 'Error saving form')
        return redirect(dashboard)
    return redirect(dashboard)


@login_required(login_url='/login/')
def edit_projects(request, id):
    proj = ProjectDetail.objects.filter(id=id)
    if request.method == "POST":
        instance = get_object_or_404(ProjectDetail, id=id)
        form = ProjectDetailForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(projects)
    context = {
        'proj': proj,
    }
    return render(request, 'edit_projects.html', context)


@login_required(login_url='/login/')
def edit_project_details(request, id):
    activities = ProjectActivitiesDetail.objects.filter(id=id)
    if request.method == "POST":
        instance = get_object_or_404(ProjectActivitiesDetail, id=id)
        proj_name = request.POST.get("proj_name")
        form = ProjectActivitiesDetailForm(request.POST or None,
                                           instance=instance)
        if form.is_valid():
            form.save()
            proj_activities = ProjectActivitiesDetail.objects.filter(
                proj_name=proj_name)
            context = {"proj_name": proj_name, "proj_activities": proj_activities}
            return render(request, 'project_detail.html', context)
    context = {
        'Activities': activities,
    }
    return render(request, 'edit_project_detail.html', context)


@login_required(login_url='/login/')
def edit_work_report(request, id):
    reports = WorkReport.objects.filter(id=id)
    if request.method == "POST":
        instance = get_object_or_404(WorkReport, id=id)
        form = WorkReportForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(dashboard)
    context = {
        'reports': reports,
    }
    return render(request, 'edit_work_report.html', context)


@login_required(login_url='/login/')
def delete_project(request, id):
    data = ProjectDetail.objects.filter(id=id)
    for i in data:
        name = i.proj_name
    ProjectActivitiesDetail.objects.filter(proj_name=name).delete()
    ProjectDetail.objects.filter(id=id).delete()
    return redirect(projects)


@login_required(login_url='/login/')
def delete_project_feature(request, id):
    proj_feature = ProjectActivitiesDetail.objects.filter(id=id)
    for i in proj_feature:
        proj_name = i.proj_name
    name = proj_name
    ProjectActivitiesDetail.objects.filter(id=id).delete()
    features = ProjectActivitiesDetail.objects.filter(proj_name=name)
    context = {"proj_name": name, "proj_feature": features}
    return render(request, 'project_detail.html', context)


@login_required(login_url='/login/')
def delete_report(request, id):
    WorkReport.objects.filter(id=id).delete()
    return redirect(dashboard)


@login_required(login_url='/login/')
def download_excel_data(request):
    if request.method == "POST":
        date = request.POST.get("date")
        print(date)
    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    #decide file name
    response['Content-Disposition'] = 'attachment; filename="WorkReport.xls"'

    #creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    #adding sheet
    ws = wb.add_sheet("sheet1")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()

    # headers are bold
    font_style.font.bold = True

    #column header names, you can use your own headers here
    columns = [
        'Sr.no',
        'Emp Code',
        'Resource Name',
        'Skill',
        'Actual Hours',
        'Date',
        'Work Details',
        'Remark',
        'Clients',
    ]

    #write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)


# Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #get your data, from database or from a text file...
    data = WorkReport.objects.filter(date=date)  #dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, row_num, font_style)
        ws.write(row_num, 1, my_row.emp_code, font_style)
        ws.write(row_num, 2, my_row.resource_name, font_style)
        ws.write(row_num, 3, my_row.skill, font_style)
        ws.write(row_num, 4, my_row.actual_hours, font_style)
        ws.write(row_num, 5, my_row.date, font_style)
        ws.write(row_num, 6, my_row.work_details, font_style)
        ws.write(row_num, 7, my_row.remark, font_style)
        ws.write(row_num, 8, my_row.clients, font_style)

    wb.save(response)
    return response