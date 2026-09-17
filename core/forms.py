from django import forms
from .models import JobPostings

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPostings
        fields = [
            'JobTitle',
            'JobDescription',
            'JobLocation',
            'JobRequirements',
            'JobType',
            'ApplicationDeadline',
            'ManpowerRequired',
            'SalaryType',
            'SalaryManual',
            'SalaryRangeMin',
            'SalaryRangeMax',
        ]


from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['Name', 'CompanyEmail', 'CompanyPhone']


from django import forms
from .models import JobSeekers

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = JobSeekers
        fields = ['profile_picture']

from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['Name', 'CompanyEmail', 'CompanyPhone', 'CompanyAddress', 'CompanyIndustry', 'CompanySize', 'ContactPersonName', 'ContactPersonEmail', 'ContactPersonPhone', 'logo']  # Add 'logo' here

    logo = forms.ImageField(required=False) 
