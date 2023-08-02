from django.forms import FileField, Form, ModelForm
from .models import HiredEmployee, Job, Department

class UploadFile(Form):
    file = FileField()

class HiredEmployeeForm(ModelForm):
    class Meta:
        model = HiredEmployee
        fields = ["employee_id", "name", "datetime", "department_id", "job_id"]

class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ["department_id", "department"]

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ["job_id", "job"]