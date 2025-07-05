from django import forms
from .models import Bug
from django.contrib.auth.models import User

class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        exclude = ['bugcode', 'user', 'created_by', 'created_at', 'updated_at', 'updated_by', 'contact_number']

    def __init__(self, *args, user_role=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Define fields for each role
        tester_fields = ['info', 'screenshot', 'status']
        developer_fields = ['fixed_by', 'sprint', 'platform', 'status']

        # Disable fields based on user role
        if user_role == 'developer':
            for field in self.fields:
                if field not in developer_fields:
                    self.fields[field].disabled = True
            self.fields['status'].choices = [
                ('Open', 'Open'),
                ('In Progress', 'In Progress'),
                ('Fixed', 'Fixed'),
            ]

        elif user_role == 'tester':
            for field in self.fields:
                if field not in tester_fields:
                    self.fields[field].disabled = True
                    self.fields[field].required = False
            self.fields['status'].choices = [
                ('Open', 'Open'),
                ('Closed', 'Closed'),
            ]

class ExcelUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.endswith('.xlsx'):
            raise forms.ValidationError("Invalid file type. Please upload an .xlsx file.")
        return file
