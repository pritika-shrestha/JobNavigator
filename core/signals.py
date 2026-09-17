
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.urls import reverse
# from .models import Application, Notification

# @receiver(post_save, sender=Application)
# def notify_employer_on_application(sender, instance, created, **kwargs):
#     if created:
#         job_seeker = instance.job_seeker
#         job_posting = instance.job_posting
#         company = job_posting.company

#         if company:
#             #  Generate profile link using the Application ID
#             profile_link = f"http://yourwebsite.com/jobseeker/{job_seeker.id}/profile/"

#             #  Create a notification for the employer
#             notification_message = f"{job_seeker.full_name} applied for your job post '{job_posting.JobTitle}'. "\
#                                    f"<a href='{profile_link}'>View Profile</a>"
#             Notification.objects.create(company=company, message=notification_message, is_read=False)
