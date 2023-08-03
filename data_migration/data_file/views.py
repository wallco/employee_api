from django.shortcuts import render
from django.views.generic.base import View
from io import TextIOWrapper
from .models import HiredEmployee, Job, Department
from .forms import UploadFile
from django.db import connection


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
    
class HiringsView(View):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""SELECT    d.department as Department, 
                                        j.job as Job,
                                        count(t1.employee_id) as Q1, 
                                        count(t2.employee_id) as Q2, 
                                        count(t3.employee_id) as Q3, 
                                        count(t4.employee_id) as Q4
                                    FROM data_file_hiredemployee t1
                                    LEFT JOIN data_file_hiredemployee t2
                                        on t1.department_id = t2.department_id and t1.job_id = t2.job_id and strftime('%Y', t2.datetime) = '2021' and strftime('%m', t2.datetime) in ('04','05','06')
                                    LEFT JOIN data_file_hiredemployee t3
                                        on t1.department_id = t3.department_id and t1.job_id = t3.job_id and strftime('%Y', t3.datetime) = '2021' and strftime('%m', t3.datetime) in ('07','08','09')
                                    LEFT JOIN data_file_hiredemployee t4
                                        on t1.department_id = t4.department_id and t1.job_id = t4.job_id and strftime('%Y', t4.datetime) = '2021' and strftime('%m', t4.datetime) in ('10','11','12')
                                    LEFT JOIN data_file_department d
                                        on t1.department_id = d.department_id
                                    LEFT JOIN data_file_job j
                                        on t1.job_id = j.job_id
                                    WHERE strftime('%Y', t1.datetime) = '2021' AND strftime('%m', t1.datetime) in ('01','02','03')
                                    GROUP BY 1, 2
                                    ORDER BY 1, 2;""")
            hirings_2021 = cursor.fetchall()
        return render(request, "hirings.html", {"items": hirings_2021})