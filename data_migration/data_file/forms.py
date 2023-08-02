from django.forms import FileField, Form, ChoiceField

class UploadFile(Form):
    file = FileField()
    #file_type = ChoiceField(choices = ('Employees', 'Departments', 'Jobs'))