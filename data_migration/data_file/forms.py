from django.forms import FileField, Form, ChoiceField
from .models import Product

class FileType(Form):
    file_type = ChoiceField(choices = ('Employees', 'Departments', 'Jobs'))

class UploadFile(Form):
    file = FileField()