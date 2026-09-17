from core.models import JobSeekers, JobPostings, Application
from django.utils import timezone

# Define application data
application_data = [
    (1, 1, 'Pending'),
    (2, 2, 'Accepted'),
    (3, 3, 'Rejected'),
    (4, 4, 'Pending'),
    (5, 5, 'Pending'),
]

# Assuming job_seekers and job_postings are already in the database
job_seekers = JobSeekers.objects.all()
job_postings = JobPostings.objects.all()

# Inserting application data
application_objects = []

for data in application_data:
    job_seeker = job_seekers.get(id=data[0])  # Get JobSeeker based on ID
    job_posting = job_postings.get(id=data[1])  # Get JobPosting based on ID
    status = data[2]

    # Create Application instance
    application = Application(
        ApplicationID=f"APP{data[0]}-{data[1]}",  # Example: APP1-1 for job_seeker 1 and job_posting 1
        job_seeker=job_seeker,
        job_posting=job_posting,
        AppliedAt=timezone.now(),  # Use current timestamp
        Status=status
    )

    # Add the application object to the list
    application_objects.append(application)

# Bulk create applications
Application.objects.bulk_create(application_objects)
print(f"{len(application_objects)} applications created.")
