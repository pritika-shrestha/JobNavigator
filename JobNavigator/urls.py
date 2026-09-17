from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView 
import os
from core import views  # Correct import based on your app name
from core.views import EmployerCVView  # Ensure this is the class
from core.views import JobSeekerCVView,RecommendationsView
from core.views import   update_contact_profile,upload_company_logo,update_company_profile, employer_view_jobseeker_profile,update_application_status,  update_jobseeker_profile,manage_jobs_view,delete_job,edit_job,dismiss_notification,notification_list,notification_detail,jobseeker_profile,company_profile,apply_for_job,search_jobs,upload_profile_picture
from  core.views import (
    CustomPasswordResetView, CustomPasswordResetConfirmView,
    CustomPasswordResetDoneView, CustomPasswordResetCompleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('jobseeker/cv/',JobSeekerCVView.as_view(), name='jobseekercv'),  # Job Seekercv
    path('employer/cv/',EmployerCVView.as_view(), name='employercv'),  # Employer cv
    path('jobseeker/dashboard/', views.JobSeekerDashboardView.as_view(), name='jobseeker_dashboard'),
    path('employer/dashboard/', views.EmployerDashboardView.as_view(), name='employer_dashboard'),
    path('', views.HomePage, name='home'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('company/manage-jobs/',manage_jobs_view, name='company_manage_jobs'),
    path('company/post-job/',views.post_job, name='company_post_job'),
    path('edit-job/<int:job_id>/', edit_job, name='edit_job'),
    path('delete-job/', delete_job, name='delete_job'),
    path('notifications/', notification_list, name='notifications'),
    # path('jobseeker/notifications/',JobSeekerNotificationsView.as_view(), name='jobseeker_notifications'),
    path('jobseeker/recommendations/',RecommendationsView.as_view(), name='jobseeker_recommendations'),
    path('jobseeker/profile/',views.jobseeker_profile, name='jobseeker_profile'),
    path('company/profile/', company_profile, name='company_profile'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    # path('add_job_alert/', views.AddJobAlertView.as_view(), name='add_job_alert'),
    path('search/', views.search_jobs, name='search_jobs'),
    path('job_search_suggestions/', views.job_search_suggestions, name='job_search_suggestions'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('notifications/<int:notification_id>/', notification_detail, name='notification_detail'),
    path('notifications/dismiss/<int:notification_id>/', dismiss_notification, name='dismiss_notification'),
    path('update-application-status/<int:application_id>/', update_application_status, name='update_application_status'),
    path('update-profile/', update_jobseeker_profile, name='update_jobseeker_profile'),
    path('employer/jobseeker/profile/<int:jobseeker_id>/', employer_view_jobseeker_profile, name='employer_jobseeker_profile'),
    path('upload-profile-picture/', upload_profile_picture, name='upload_profile_picture'),
    path('update_company_profile/', update_company_profile, name='update_company_profile'),
    path('upload_company_logo/', upload_company_logo, name='upload_company_logo'),
    path('update-contact-profile/', update_contact_profile, name='update_contact_profile'),
    path('recommendations/', views.job_recommendations, name='jobseeker_recommendations'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))

# Ensure this is included for local development
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)