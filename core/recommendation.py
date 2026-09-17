# from .models import JobSeekers, JobPostings

# def recommend_jobs(seeker_id):
#     try:
#         # Get the job seeker by ID
#         seeker = JobSeekers.objects.get(id=seeker_id)
#     except JobSeekers.DoesNotExist:
#         raise ValueError(f"Job seeker with ID {seeker_id} does not exist.")

#     # Get all job postings
#     jobs = JobPostings.objects.all()

#     # Extract skills and location from the job seeker
#     seeker_skills = set(seeker.technical_skills.split(',')) if seeker.technical_skills else set()
#     seeker_location = seeker.location

#     recommended_jobs = []

#     for job in jobs:
#         relevance = 0

#         # Match technical skills
#         if job.JobRequirements and seeker.technical_skills:
#             relevance += match_skills(job.JobRequirements, seeker.technical_skills)

#         # Match interpersonal skills
#         if job.JobRequirements and seeker.interpersonal_skills:
#             relevance += match_skills(job.JobRequirements, seeker.interpersonal_skills)

#         # Match location
#         if job.JobLocation and seeker.location:
#             relevance += 5 if job.JobLocation.lower() == seeker.location.lower() else 0

#         # Add more matching criteria here (e.g., salary, job type, etc.)

#         if relevance > 0:
#             recommended_jobs.append({
#                 'job': job,
#                 'relevance': relevance
#             })

#     # Sort the jobs by relevance score
#     recommended_jobs.sort(key=lambda x: x['relevance'], reverse=True)

#     return recommended_jobs

# def match_skills(job_requirements, seeker_skills):
#     """
#     Match skills between job requirements and job seeker's skills.
#     """
#     job_skills = [skill.strip().lower() for skill in job_requirements.split(',')]
#     seeker_skills = [skill.strip().lower() for skill in seeker_skills.split(',')]
#     common_skills = set(job_skills).intersection(set(seeker_skills))
#     return len(common_skills) * 10  # Reward 10 points for each matching skill






# from .models import JobSeekers, JobPostings

# def recommend_jobs(seeker_id, threshold=10):
#     try:
#         # Get the job seeker by ID
#         seeker = JobSeekers.objects.get(id=seeker_id)
#     except JobSeekers.DoesNotExist:
#         raise ValueError(f"Job seeker with ID {seeker_id} does not exist.")

#     # Get all job postings
#     jobs = JobPostings.objects.all()

#     # Extract skills and location from the job seeker
#     seeker_skills = set(seeker.technical_skills.split(',')) if seeker.technical_skills else set()
#     seeker_location = seeker.location

#     recommended_jobs = []

#     for job in jobs:
#         relevance = 0

#         # Match technical skills
#         if job.JobRequirements and seeker.technical_skills:
#             relevance += match_skills(job.JobRequirements, seeker.technical_skills)

#         # Match interpersonal skills
#         if job.JobRequirements and seeker.interpersonal_skills:
#             relevance += match_skills(job.JobRequirements, seeker.interpersonal_skills)

#         # Match location
#         if job.JobLocation and seeker.location:
#             relevance += 5 if job.JobLocation.lower() == seeker.location.lower() else 0

#         # Add more matching criteria here (e.g., salary, job type, etc.)

#         # Only recommend jobs that meet the threshold
#         if relevance >= threshold:
#             recommended_jobs.append({
#                 'job': job,
#                 'relevance': relevance
#             })

#     # Sort the jobs by relevance score
#     recommended_jobs.sort(key=lambda x: x['relevance'], reverse=True)

#     return recommended_jobs

# def match_skills(job_requirements, seeker_skills):
#     """
#     Match skills between job requirements and job seeker's skills.
#     """
#     job_skills = [skill.strip().lower() for skill in job_requirements.split(',')]
#     seeker_skills = [skill.strip().lower() for skill in seeker_skills.split(',')]
#     common_skills = set(job_skills).intersection(set(seeker_skills))
#     return len(common_skills) * 10  # Reward 10 points for each matching skill


from .models import JobSeekers, JobPostings

def recommend_jobs(seeker_id, threshold=6):
    try:
        # Get the job seeker by ID
        seeker = JobSeekers.objects.get(id=seeker_id)
    except JobSeekers.DoesNotExist:
        raise ValueError(f"Job seeker with ID {seeker_id} does not exist.")

    # Get all job postings
    jobs = JobPostings.objects.all()

    # Extract and combine skills from the job seeker
    seeker_technical_skills = set(skill.strip().lower() for skill in seeker.technical_skills.split(',')) if seeker.technical_skills else set()
    seeker_interpersonal_skills = set(skill.strip().lower() for skill in seeker.interpersonal_skills.split(',')) if seeker.interpersonal_skills else set()
    
    # Combine technical and interpersonal skills into a single set
    seeker_combined_skills = seeker_technical_skills.union(seeker_interpersonal_skills)
    
    # Extract location from the job seeker
    seeker_location = seeker.location.lower() if seeker.location else None

    # Debugging: Print seeker details
    print(f"Seeker Combined Skills: {seeker_combined_skills}")
    print(f"Seeker Location: {seeker_location}")

    recommended_jobs = []

    for job in jobs:
        relevance = 0

        # Debugging: Print job details
        print(f"Job ID: {job.id}, Requirements: {job.JobRequirements}, Location: {job.JobLocation}")

        # Match combined skills against job requirements
        if job.JobRequirements and seeker_combined_skills:
            relevance += match_skills(job.JobRequirements, seeker_combined_skills)

        # Match location
        if job.JobLocation and seeker_location:
            relevance += 5 if job.JobLocation.lower() == seeker_location else 0

        # Debugging: Print relevance score
        print(f"Relevance Score for Job ID {job.id}: {relevance}")

        # Only recommend jobs that meet the threshold
        if relevance >= threshold:
            recommended_jobs.append({
                'job': job,
                'relevance': relevance
            })

    # Sort the jobs by relevance score
    recommended_jobs.sort(key=lambda x: x['relevance'], reverse=True)

    # Debugging: Print recommended jobs
    print(f"Recommended Jobs: {recommended_jobs}")

    return recommended_jobs

def match_skills(job_requirements, seeker_skills):
    """
    Match skills between job requirements and job seeker's skills.
    """
    job_skills = [skill.strip().lower() for skill in job_requirements.split(',')]
    common_skills = set(job_skills).intersection(seeker_skills)
    return len(common_skills) * 10  # Reward 10 points for each matching skill