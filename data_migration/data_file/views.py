from django.shortcuts import render
from django.views.generic.base import View
from io import TextIOWrapper
from .models import HiredEmployee, Job, Department
from .forms import UploadFile
from django.db import connection


class UploadView(View):
    #Presents the upload form when accessed
    def get(self, request, *args, **kwargs):
        return render(request, "index.html", {"form": UploadFile()})
    
    def post(self, request, *args, **kwargs):
        #Retrieves the identifier of which table is the data being uploaded to
        load_type = request.POST['type']
        #Initializes row collection
        items = []
        #Retrieves file and reads rows
        file = request.FILES["file"]
        rows = TextIOWrapper(file, encoding="utf-8", newline="")
        #Controls the flow according to the data type, retrieves its corresponding attributes, constructing a Django Model object with them,
        #appending to the items list and finally bulk-upserting when the loop ends
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
        #Returns the user to the same upload page
        return render(request, "index.html", {"form": UploadFile()})
    
class HiringsView(View):
    #Runs query and then passes the corresponding result to the table template
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""  with q1 as (select department_id, job_id, count(employee_id) as employee_count 
                                from data_file_hiredemployee 
                                where strftime('%Y', datetime) = '2021' and strftime('%m', datetime) in ('01', '02', '03') group by 1,2),
                        q2 as (select department_id, job_id, count(employee_id) as employee_count 
                                from data_file_hiredemployee 
                                where strftime('%Y', datetime) = '2021' and strftime('%m', datetime) in ('04', '05', '06') group by 1,2),
                        q3 as (select department_id, job_id, count(employee_id) as employee_count 
                                from data_file_hiredemployee 
                                where strftime('%Y', datetime) = '2021' and strftime('%m', datetime) in ('07', '08', '09') group by 1,2),
                        q4 as (select department_id, job_id, count(employee_id) as employee_count 
                                from data_file_hiredemployee 
                                where strftime('%Y', datetime) = '2021' and strftime('%m', datetime) in ('10', '11', '12') group by 1,2)
                    select distinct d.department, 
                                    j.job, 
                                    IFNULL(q1.employee_count, 0) as q1, 
                                    IFNULL(q2.employee_count, 0) as q2, 
                                    IFNULL(q3.employee_count, 0) as q3, 
                                    IFNULL(q4.employee_count, 0) as q4
                    from data_file_hiredemployee t0
                    left join q1 q1 on (t0.department_id, t0.job_id) = (q1.department_id, q1.job_id)
                    left join q2 q2 on (t0.department_id, t0.job_id) = (q2.department_id, q2.job_id)
                    left join q3 q3 on (t0.department_id, t0.job_id) = (q3.department_id, q3.job_id)
                    left join q4 q4 on (t0.department_id, t0.job_id) = (q4.department_id, q4.job_id)
                    left join data_file_department d on t0.department_id = d.department_id
                    left join data_file_job j on t0.job_id = j.job_id
                    where not (q1.employee_count is null and q2.employee_count is null and q3.employee_count is null and q4.employee_count is null)
                    order by 1,2""")
            hirings_2021 = cursor.fetchall()
        return render(request, "hirings.html", {"items": hirings_2021})
    
class HiringsDepView(View):
    #Runs query and then passes the corresponding result to the table template
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""  with department_hires as (select department_id, count(employee_id)  as employee_count
                                        from data_file_hiredemployee
                                        where strftime('%Y', datetime) = '2021'
                                        group by 1)
                                select dh.department_id, d.department, dh.employee_count
                                from department_hires dh
                                inner join data_file_department d on d.department_id = dh.department_id
                                where dh.employee_count > (select avg(employee_count) from department_hires)
                                order by 3 desc""")
            hirings_2021_dep = cursor.fetchall()
        return render(request, "hirings_dep.html", {"items": hirings_2021_dep})