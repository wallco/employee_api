from django.forms import FileField, Form, ModelForm
from .models import HiredEmployee, Job, Department


#File form to be rendered in UploadView
class UploadFile(Form):
    file = FileField()