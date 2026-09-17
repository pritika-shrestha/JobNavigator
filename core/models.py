from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Company Model
class Company(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    CompanyID = models.IntegerField(default=1)
    Name = models.CharField(max_length=150)
    CompanyEmail = models.EmailField(max_length=255)
    CompanyPhone = models.CharField(max_length=20)
    CompanyAddress = models.TextField()
    CompanyIndustry = models.CharField(max_length=100)
    CompanySize = models.CharField(max_length=20)  # Small, Medium, Large
    ContactPersonName = models.CharField(max_length=150)
    ContactPersonEmail = models.EmailField(max_length=255)
    ContactPersonPhone = models.CharField(max_length=20)
    PasswordHash = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True,default='company_logos/default_logo.png')  # Add this line for logo


    def __str__(self):
        return self.Name

def profile_picture_path(instance, filename):
    return f'profile_pictures/{instance.user.id}/{filename}'
# JobSeekers Model
class JobSeekers(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=False, blank=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    interpersonal_skills = models.TextField(null=True, blank=True)  # Allow null values
    technical_skills = models.TextField(null=True, blank=True)  # Allow null values
    experience = models.TextField(null=True, blank=True)  # Allow null values
    education = models.TextField(null=True, blank=True)  # Allow null values
    # password = models.CharField(max_length=255)
    PasswordHash = models.CharField(max_length=255)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to=profile_picture_path, default='profile_pictures/default.png')

    def __str__(self):
        return self.full_name

# JobPostings Model
from django.db import models

class JobPostings(models.Model):
    JOB_TYPES = (
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
    )
    
    SALARY_TYPES = (
        ('Manual', 'Manual'),
        ('Range', 'Range'),
        ('Negotiable', 'Negotiable'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs', null=True, blank=True)
    JobTitle = models.CharField(max_length=255)
    JobDescription = models.TextField()
    JobLocation = models.CharField(max_length=255)
    JobRequirements = models.TextField()
    JobType = models.CharField(max_length=20, choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time')])
    ApplicationDeadline = models.DateField()
    ManpowerRequired = models.IntegerField()
    SalaryType = models.CharField(max_length=20, choices=[('Manual', 'Manual'), ('Range', 'Range'), ('Negotiable', 'Negotiable')])
    SalaryManual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Manual Salary
    SalaryRangeMin = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Salary Range Min
    SalaryRangeMax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Salary Range Max

    def __str__(self):
        return self.JobTitle


# Application Model
class Application(models.Model):
    ApplicationID = models.CharField(max_length=100, default='default_value')  # Provide a default value
    job_seeker = models.ForeignKey(JobSeekers, on_delete=models.CASCADE, null=True)  # Allow null
    job_posting = models.ForeignKey(JobPostings, on_delete=models.CASCADE, null=True)  # Allow null
    AppliedAt = models.DateTimeField(default=timezone.now)  # auto_now_add is fine here
    Status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"Application for {self.job_posting.JobTitle} by {self.job_seeker.full_name}"
    

#JobAlert Model job alert is showing some errors
# class JobAlert(models.Model):
#     AlertID = models.AutoField(primary_key=True) # AutoField for the primary key
#     job_seeker = models.ForeignKey(JobSeekers, on_delete=models.CASCADE, null=True)  # Allow null if preferences are not provided
#     Preferences = models.TextField(null=True, blank=True)  # Allow null values
#     CreatedAt = models.DateTimeField(auto_now_add=True)  # auto_now_add is fine here

#     def __str__(self):
#         return f"Alert for {self.job_seeker.full_name}"

# Admin Model
class Admin(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=150, unique=True)
    PasswordHash = models.CharField(max_length=255)
    Role = models.CharField(max_length=50)
    CreatedAt = models.DateTimeField(auto_now_add=True)  # auto_now_add is fine here

    def __str__(self):
        return self.Name

# New UserProfile model for linking User and additional user data added
# class UserProfile(models.Model):
#     USER_TYPE_CHOICES = [
#         ('seeker', 'Job Seeker'),
#         ('employer', 'Employer'),
#     ]
    
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default='seeker')
#     full_name = models.CharField(max_length=255, null=True, blank=True)  # Allow null if not provided
#     phone = models.CharField(max_length=20, null=True, blank=True)  # Allow null if not provided
#     location = models.CharField(max_length=255, null=True, blank=True)  # Allow null if not provided

#     def __str__(self):
#         return self.user.username
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default='seeker')
    full_name = models.CharField(max_length=255, null=True, blank=True)  # Allow null if not provided
    phone = models.CharField(max_length=20, null=True, blank=True)  # Allow null if not provided
    location = models.CharField(max_length=255, null=True, blank=True)  # Allow null if not provided

    # Fetching company details from the Company model
    company_name = models.CharField(max_length=150, null=True, blank=True)  # Matches Company.Name
    industry = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username  # Corrected this line


from django.db import models
from django.contrib.auth.models import User

from django.db import models
import django.db.models.deletion 

class Notification(models.Model):
    job_seeker = models.ForeignKey('JobSeekers', on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    application = models.ForeignKey('Application', on_delete=models.CASCADE, db_column='application_id')  # Explicit column name

    # def __str__(self):
    #     recipient = self.job_seeker.full_name if self.job_seeker else self.company.Name if self.company else "Unknown"
        # return f"Notification for {recipient}"
    def save(self, *args, **kwargs):
        if self.job_seeker and self.company:
            raise ValueError("A notification cannot be assigned to both a job seeker and a company.")
        if not self.job_seeker and not self.company:
            raise ValueError("A notification must be assigned to either a job seeker or a company.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.message} - {'Job Seeker' if self.job_seeker else 'Company'}"
    
from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'c_dashboard.html')

def notifications_view(request):
    return render(request, 'c_notification.html')

from django.db.models.signals import post_save
import core.signals  # Manually import signals






