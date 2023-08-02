from django.shortcuts import render
from django.views.generic.base import View
from csv import DictReader
from io import TextIOWrapper
from .models import HiredEmployee, Job, Department
from .forms import UploadFile


class UploadView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html", {"form": UploadFile()})
    
    def post(self, request, *args, **kwargs):
        load_type = request.POST['type']
        items = []
        file = request.FILES["file"]
        rows = TextIOWrapper(file, encoding="utf-8", newline="")
        if load_type == 'Submit Employees':
            for row in rows:
                list = row.split(',')
                employee_id = list[0]
                name = list[1]
                datetime = list[2]
                department_id = list[3]
                job_id = list[4].strip('\r\n')
                if name == '':
                    name = None
                if datetime == '':
                    datetime = None
                if department_id == '':
                    department_id = None
                if job_id == '':
                    job_id = None
                items.append(HiredEmployee(employee_id=employee_id, name=name, datetime=datetime, department_id = department_id, job_id = job_id))
            HiredEmployee.objects.bulk_update_or_create(items, ['name', 'datetime','department_id', 'job_id'], match_field = 'employee_id', batch_size=1000)
        elif load_type == 'Submit Jobs':
            for row in rows:
                list = row.split(',')
                job_id = list[0]
                job = list[1].strip('\r\n')
                if job == '':
                    job = None
                items.append(Job(job_id = job_id, job = job))
            Job.objects.bulk_update_or_create(items, ['job'], match_field = 'job_id')
        elif load_type == 'Submit Departments':
            for row in rows:
                list = row.split(',')
                department_id = list[0]
                department = list[1].strip('\r\n')
                if department == '':
                    department = None
                items.append(Department(department_id = department_id, department = department))
            Department.objects.bulk_update_or_create(items, ['department'], match_field = 'department_id')
        else:
            pass
        return render(request, "index.html", {"form": UploadFile()})
        