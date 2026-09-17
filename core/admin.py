from django.contrib import admin
from .models import Company, JobSeekers, JobPostings, Application, Admin, UserProfile,Notification

# Register the models with Django admin

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('Name', 'CompanyEmail', 'CompanyPhone', 'CompanyIndustry', 'CompanySize', 'ContactPersonName')
    search_fields = ('Name', 'CompanyEmail', 'CompanyPhone')
    list_filter = ('CompanyIndustry', 'CompanySize')

class JobSeekersAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'location', 'CreatedAt')
    search_fields = ('full_name', 'email', 'phone')
    list_filter = ('location', 'CreatedAt')

from django.contrib import admin
from django import forms
from .models import JobPostings

# Custom form for handling JobPostings
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

# Customize Django admin panel for JobPostings
class JobPostingsAdmin(admin.ModelAdmin):
    form = JobPostingForm  # Assign custom form

    list_display = (
        'JobTitle', 
        'JobLocation', 
        'JobType', 
        'ApplicationDeadline', 
        'ManpowerRequired', 
        'SalaryType', 
        'SalaryManual', 
        'SalaryRangeMin', 
        'SalaryRangeMax'
    )
    
    search_fields = ('JobTitle', 'JobLocation', 'JobType')
    list_filter = ('JobType', 'SalaryType', 'ApplicationDeadline')

    fieldsets = (
        (None, {
            'fields': ('JobTitle', 'JobDescription', 'JobLocation', 'JobRequirements', 'JobType', 'ApplicationDeadline', 'ManpowerRequired')
        }),
        ('Salary Information', {
            'fields': ('SalaryType', 'SalaryManual', 'SalaryRangeMin', 'SalaryRangeMax')
        }),
    )


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'job_posting', 'Status', 'AppliedAt')  # Updated field names
    search_fields = ('job_seeker__full_name', 'job_posting__JobTitle', 'Status')  # Updated field names
    list_filter = ('Status', 'AppliedAt')
    

class JobAlertAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'Preferences', 'CreatedAt')  # Updated field names
    search_fields = ('job_seeker__full_name', 'Preferences')  # Updated field names
    list_filter = ('CreatedAt',)

class AdminAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Email', 'Role', 'CreatedAt')
    search_fields = ('Name', 'Email', 'Role')
    list_filter = ('Role',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'full_name', 'phone', 'location')
    search_fields = ('user__username', 'full_name', 'phone')
    list_filter = ('user_type',)

from django.contrib import admin
from django.core.mail import send_mail
from .models import Notification, JobSeekers, Company

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['get_recipient', 'message', 'is_read', 'created_at']
    actions = ['send_notification_to_selected_seekers', 'send_notification_to_selected_companies', 
               'send_notification_to_all_seekers', 'send_notification_to_all_companies']

    def get_recipient(self, obj):
        if obj.job_seeker:
            return obj.job_seeker.full_name
        elif obj.company:
            return obj.company.Name
        return "No Recipient"

    get_recipient.short_description = "Recipient"

    def send_notification_email(self, recipient_email, recipient_name, message):
        """ Helper function to send email notifications """
        subject = "New Job Portal Notification"
        body = f"Hello {recipient_name},\n\n{message}\n\nThank you,\nJob Portal Team"
        send_mail(subject, body, 'your-email@gmail.com', [recipient_email], fail_silently=False)

    def send_notification_to_selected_seekers(self, request, queryset):
        selected_seekers = JobSeekers.objects.filter(id__in=queryset.values_list('job_seeker', flat=True))
        for seeker in selected_seekers:
            message = f"Admin message for {seeker.full_name}."
            Notification.objects.create(job_seeker=seeker, message=message,is_read=False)
            
            if seeker.user.email:  # Check if the user has an email
                self.send_notification_email(seeker.user.email, seeker.full_name, message)

        self.message_user(request, f"Notifications sent to {selected_seekers.count()} job seekers.")

    def send_notification_to_selected_companies(self, request, queryset):
        selected_companies = Company.objects.filter(id__in=queryset.values_list('company', flat=True))
        for company in selected_companies:
            message = f"Admin message for {company.Name}."
            Notification.objects.create(company=company, message=message,is_read=False)
            
            if company.user.email:  # Check if the company has an email
                self.send_notification_email(company.user.email, company.Name, message)

        self.message_user(request, f"Notifications sent to {selected_companies.count()} companies.")

    def send_notification_to_all_seekers(self, request, queryset=None):
        job_seekers = JobSeekers.objects.all()
        for seeker in job_seekers:
            message = "Notification for job seekers."
            Notification.objects.create(job_seeker=seeker, message=message,is_read=False)
            
            if seeker.user.email:
                self.send_notification_email(seeker.user.email, seeker.full_name, message)

        self.message_user(request, "Notifications sent to all job seekers.")

    def send_notification_to_all_companies(self, request, queryset=None):
        companies = Company.objects.all()
        for company in companies:
            message = "Notification for companies."
            Notification.objects.create(company=company, message=message,is_read=False)
            
            if company.user.email:
                self.send_notification_email(company.user.email, company.Name, message)

        self.message_user(request, "Notifications sent to all companies.")

    send_notification_to_selected_seekers.short_description = "Send notification to selected job seekers"
    send_notification_to_selected_companies.short_description = "Send notification to selected companies"
    send_notification_to_all_seekers.short_description = "Send notification to all job seekers"
    send_notification_to_all_companies.short_description = "Send notification to all companies"


# Register models with their respective admin classes
admin.site.register(Company, CompanyAdmin)
admin.site.register(JobSeekers, JobSeekersAdmin)
admin.site.register(JobPostings, JobPostingsAdmin)
admin.site.register(Application, ApplicationAdmin)
# admin.site.register(JobAlert, JobAlertAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Notification, NotificationAdmin)
