from django.forms import FileField, Form, ModelForm
from .models import Product


class UploadEmployees(Form):
    employee_file = FileField()

class UploadJobs(Form):
    job_file = FileField()

class UploadDepartments(Form):
    department_file = FileField()