from django.shortcuts import redirect, HttpResponse, get_object_or_404
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import JobSeekers, Company, JobPostings, Application
from .models import UserProfile
import json
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_protect
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


# Utility function to validate email
def validate_email_address(email):
    try:
        validate_email(email)
    except ValidationError:
        return False
    return True


# Utility function for creating users
def create_user(username, email, password, is_staff):
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = is_staff  # is_staff determines if the user is an employer  (is_staff=True)  or a job seeker  (is_staff=false) 
        user.save()
        return user
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from .models import UserProfile, JobSeekers, Company

@csrf_protect
def SignupPage(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')  # 'seeker' or 'employer'
        fullname = request.POST.get('fullname') if user_type == 'seeker' else request.POST.get('company_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        #  **Validation Checks**
        if not fullname or not email or not pass1 or not pass2:
            return JsonResponse({"error": "All fields are required!"}, status=400)

        if pass1 != pass2:
            return JsonResponse({"error": "Passwords do not match!"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email is already registered!"}, status=400)

        # Generate a unique username
        username = fullname.split()[0].capitalize()
        if User.objects.filter(username=username).exists():
            username += str(User.objects.count() + 1)

        # **Create the User**
        user = User.objects.create_user(username=username, email=email, password=pass1)
        user.is_active = True  # Activate the account immediately
        user.save()

        #  **Create UserProfile**
        user_profile = UserProfile.objects.create(
            user=user,
            user_type=user_type,
            full_name=fullname
        )
        user_profile.save()

        #  **Automatically Create Job Seeker or Employer Profile**
        if user_type == 'seeker':
            JobSeekers.objects.create(
                user=user,
                full_name=fullname,
                email=email,
                phone="",
                location="",
                PasswordHash=user.password  #  You may want to use Django's hashing method instead
            )
        elif user_type == 'employer':
            Company.objects.create(
                user=user,
                Name=fullname,
                CompanyEmail=email,
                CompanyPhone="",
                CompanyAddress="",
                CompanyIndustry="",
                CompanySize="",
                ContactPersonName="",
                ContactPersonEmail=email,
                ContactPersonPhone="",
                PasswordHash=user.password  #  Same hashing concern
            )

        #  **Redirect Based on User Type**
        if user_type == 'seeker':
            return redirect('jobseekercv')  # Redirect to Job Seeker's CV page
        elif user_type == 'employer':
            return redirect('employercv')  # Redirect to Employer's CV page
        
        return redirect("login")  # Default redirection to login page

    return render(request, 'signup.html')

from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render
import json
from .models import UserProfile  
from django.contrib.auth.models import User  

@csrf_protect
def LoginPage(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            user_type = data.get('user_type', '').strip().lower()

            print("Received Data:", email, password, user_type)  # Debugging

            if not email or not password or not user_type:
                return JsonResponse({"error": "All fields are required!"}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({"error": "Email is not registered!"}, status=400)
            print(" User found:", user.username)  # Debugging

            user_profile = UserProfile.objects.filter(user=user).first()
            if not user_profile:
                return JsonResponse({"error": "User profile not found!"}, status=400)

            if user_profile.user_type.lower() != user_type:
                return JsonResponse({"error": "User type mismatch!"}, status=400)
            
            authenticated_user = authenticate(request, username=email, password=password)
            if authenticated_user is None:
                return JsonResponse({"error": "Invalid email or password!"}, status=400)
            # ✅ Fix: Make sure user session is stored
            login(request, authenticated_user)
            request.session.save()
            print(f"✅ User {authenticated_user.username} logged in. Session ID: {request.session.session_key}")
            redirect_url = "jobseeker/dashboard/" if user_type == "seeker" else "employer/dashboard/"
            return JsonResponse({"success": True, "redirect_url": redirect_url}, status=200)

        except Exception as e:
            print(" SERVER ERROR:", str(e))  # This will print the actual error in the terminal
            return JsonResponse({"error": "Server error, check logs!"}, status=500)
    request.session.flush()
    return render(request, 'login.html')


def HomePage(request):
    return render(request, 'index.html')

def LogoutPage(request):
    logout(request)
    return redirect('home')

from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = 'about.html'


# from django.shortcuts import render, redirect
# from django.views import View
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import ensure_csrf_cookie
# from django.http import JsonResponse


# @method_decorator(ensure_csrf_cookie, name='dispatch')
# class JobSeekerCVView(View):
    # def get(self, request, *args, **kwargs):
    #     user = request.user
    #     job_seeker = JobSeekers.objects.filter(user=user).first() 
    #     return render(request, 'jobseekercv.html')
    

    # def post(self, request, *args, **kwargs):
    #     user = request.user 
    #     # Ensure the UserProfile exists for the user, create it if missing
    #     user_profile, created = UserProfile.objects.get_or_create(user=user)

    #     # If the profile is created, set the user_type to 'seeker'
    #     if created:
    #         user_profile.user_type = 'seeker'
    #         user_profile.save()

    #     # If the profile already exists, check and update user_type if necessary
    #     if user_profile.user_type != 'seeker':
    #         user_profile.user_type = 'seeker'
    #         user_profile.save()


    #     full_name = request.POST.get('fullName')  # Get full name from CV form
    #     email = request.POST.get('email')
    #     phone = request.POST.get('phone')
    #     location = request.POST.get('location')
    #     interpersonal_skills = request.POST.get('skills')  # Matches form
    #     technical_skills = request.POST.get('technicalSkills')
    #     experience = request.POST.get('experience')
    #     education = request.POST.get('education')
        
    #     # Create the JobSeeker profile directly
    #     job_seeker = JobSeekers.objects.create(
    #         user=user,
    #         full_name=full_name ,  # Using username as full name if needed
    #         email=email,
    #         phone=phone,
    #         location=location,
    #         interpersonal_skills=interpersonal_skills,
    #         technical_skills=technical_skills,
    #         experience=experience,
    #         education=education,
    #         # password=request.user.password  # Not ideal, should hash passwords
    #     )
    #     job_seeker.save()
    # 
    
    from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from core.models import JobSeekers
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

@method_decorator(login_required, name='dispatch')  # Ensures user is logged in before accessing
class JobSeekerCVView(View):

    def get(self, request, *args, **kwargs):
        """ Load Job Seeker CV page with existing profile data. """
        print(f"DEBUG: Fetching profile for user {request.user.username}")

        # Ensure the user has a JobSeeker profile
        job_seeker = JobSeekers.objects.filter(user=request.user).first()

        if not job_seeker:
            print("❌ No JobSeeker profile found, creating a new one...")
            job_seeker = JobSeekers.objects.create(user=request.user)

        return render(request, 'jobseekercv.html', {'jobseeker': job_seeker})

    def post(self, request, *args, **kwargs):
        """ Handle Job Seeker CV submission and save profile details. """

        # Ensure user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User is not authenticated'}, status=400)

        print(f"✅ Processing CV update for user {request.user.username}")

        # Fetch or create the JobSeeker profile
        job_seeker, created = JobSeekers.objects.get_or_create(user=request.user)

        # Debugging
        if created:
            print(f"✅ New JobSeeker profile created for {request.user.username}")
        else:
            print(f"ℹ️ Updating existing profile for {request.user.username}")

        # Retrieve form data from request
        job_seeker.full_name = request.POST.get('fullName', job_seeker.full_name)
        job_seeker.email = request.POST.get('email', job_seeker.email)
        job_seeker.phone = request.POST.get('phone', job_seeker.phone)
        job_seeker.location = request.POST.get('location', job_seeker.location)
        job_seeker.interpersonal_skills = request.POST.get('skills', job_seeker.interpersonal_skills)
        job_seeker.technical_skills = request.POST.get('technicalSkills', job_seeker.technical_skills)
        job_seeker.experience = request.POST.get('experience', job_seeker.experience)
        job_seeker.education = request.POST.get('education', job_seeker.education)

        # Save the updated profile
        job_seeker.save()
        print(f"✅ Job Seeker Profile Updated: {job_seeker}")

        # Send verification email
        uid = urlsafe_base64_encode(force_bytes(request.user.pk))
        token = default_token_generator.make_token(request.user)
        verification_url = f"http://{get_current_site(request).domain}/verify/{uid}/{token}/"

        subject = "Account Verification"
        message = f"""
        Hello {request.user.username}, 

        Thank you for completing your profile! Please verify your email to activate your account:

        {verification_url}

        If you did not sign up, please ignore this email.

        Best Regards,
        JobNavigator Team
        """
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [job_seeker.email])  # Use the correct email

        return JsonResponse({
            "success": True,
            "message": "Your CV has been saved! Please check your email to verify your account before logging in.",
            "redirect_url": "/jobseeker_profile/"  # Redirect to the profile page
        }, status=200)

from django.views import View
from django.shortcuts import render
from .models import JobPostings

class JobSeekerDashboardView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        print(f" DEBUG: Logged-in user = {request.user} (ID: {request.user.id})")  # Debugging

        job_seeker = JobSeekers.objects.filter(user=request.user).first()
        jobseeker_id = job_seeker.id if job_seeker else None

        print(f"DEBUG: job_seeker = {job_seeker}")  # Check if job_seeker exists
        print(f"DEBUG: jobseeker_id = {jobseeker_id}")  # Check if jobseeker_id is correctly assigned

        job_postings = JobPostings.objects.all().order_by('-ApplicationDeadline')

        return render(request, 'jobseekerdashboard.html', {
            'job_postings': job_postings,
            'jobseeker_id': jobseeker_id,
        })


    
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import JobSeekers, JobPostings,Application

@login_required
def apply_for_job(request, job_id):
    if request.method == 'POST':
        print(f"Applying for job with ID: {job_id}") 
        # Get the Job Posting and Job Seeker
        job = get_object_or_404(JobPostings, id=job_id)
        job_seeker = JobSeekers.objects.filter(user=request.user).first()
         

        print(f"🔍 Found Job: {job.JobTitle} at {job.JobLocation}")
        print(f"👤 Job Seeker: {job_seeker.full_name}, Email: {job_seeker.email}")

        # Check if the user has already applied for this job
        if Application.objects.filter(job_posting=job, job_seeker=job_seeker).exists():
           return JsonResponse({'success': False, 'message': 'You have already applied for this job.'})
        
        # If not, create a new application
        Application.objects.create(job_posting=job, job_seeker=job_seeker)
        return JsonResponse({'success': True, 'message': 'Successfully applied for the job!'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
# from django.views import View
from django.shortcuts import render


# @login_required  # This ensures the user is logged in before accessing the view
class EmployerCVView(View):
    # def get(self, request, *args, **kwargs):
    #     return render(request, 'employercv.html')
        
    # def post(self, request,*args, **kwargs):
    #     user = request.user 
            
    #         # Ensure the UserProfile exists for the user, create it if missing
    #     user_profile, created = UserProfile.objects.get_or_create(user=user)

    #     if user_profile.user_type != 'employer':
    #       user_profile.user_type = 'employer'
    #       user_profile.save()
    #       user_profile.refresh_from_db()

    #     # Ensure the user is an employer
    #     if user_profile.user_type != 'employer':
    #         return JsonResponse({"error": "Invalid user type!"}, status=400)

    #     company_name = request.POST.get('companyName')
    #     company_email = request.POST.get('companyEmail')
    #     phone = request.POST.get('companyPhone')
    #     address = request.POST.get('companyAddress')
    #     industry = request.POST.get('companyIndustry')
    #     company_size = request.POST.get('companySize')
    #     contact_person_name = request.POST.get('contactPersonName')
    #     contact_person_email = request.POST.get('contactPersonEmail')
    #     contact_person_phone = request.POST.get('contactPersonPhone')

        
    #     company = Company.objects.create(
    #         user=user,
    #         Name=company_name,  # Ensure no leading/trailing spaces
    #         CompanyEmail=company_email,
    #         CompanyPhone=phone,
    #         CompanyAddress=address,
    #         CompanyIndustry=industry,
    #         CompanySize=company_size,
    #         ContactPersonName=contact_person_name,
    #         ContactPersonEmail=contact_person_email,
    #         ContactPersonPhone=contact_person_phone,
    #         PasswordHash=request.user.password  # Should be hashed in production
    #     )
        
    #     company.save()
        
    def get(self, request, *args, **kwargs):
        user = request.user
        company = Company.objects.filter(user=user).first()  # Fetch existing company
        return render(request, 'employercv.html', {'company': company})

    def post(self, request, *args, **kwargs):
        user = request.user
        company, created = Company.objects.get_or_create(user=user)  # Fetch or create

        company.Name = request.POST.get('companyName', company.Name)
        company.CompanyEmail = request.POST.get('companyEmail', company.CompanyEmail)
        company.CompanyPhone = request.POST.get('companyPhone', company.CompanyPhone)
        company.CompanyAddress = request.POST.get('companyAddress', company.CompanyAddress)
        company.CompanyIndustry = request.POST.get('companyIndustry', company.CompanyIndustry)
        company.CompanySize = request.POST.get('companySize', company.CompanySize)
        company.ContactPersonName = request.POST.get('contactPersonName', company.ContactPersonName)
        company.ContactPersonEmail = request.POST.get('contactPersonEmail', company.ContactPersonEmail)
        company.ContactPersonPhone = request.POST.get('contactPersonPhone', company.ContactPersonPhone)

        company.save()

        print("Employer (Company) Profile Created:", company)
        # ✅ Send the verification email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verification_url = f"http://{get_current_site(request).domain}/verify/{uid}/{token}/"

        subject = "Account Verification"
        message = f"""
        Hello {user.username},

        Thank you for completing your profile! Please verify your email to activate your account:

        {verification_url}

        If you did not sign up, please ignore this email.

        Best Regards,
        JobNavigator Team
        """
        
        # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [company_email])
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [company.CompanyEmail])  # ✅ Uses the correct company email

        # ✅ Redirect to login instead of dashboard
        return JsonResponse({
            "success": True,
            "message": "Your company profile has been saved! Please check your email to verify your account before logging in.",
            "redirect_url": "/login/"
        }, status=200)
    
    
from django.shortcuts import render
from django.views import View
from .models import Company, JobPostings, Application

class EmployerDashboardView(View):
    def get(self, request):
        # Debugging log for logged-in user
        print(f"Logged-in User: {request.user} (ID: {request.user.id})")
        
        # Get the company for the logged-in user
        company = Company.objects.filter(user=request.user).first()

        if company:
            # Total number of jobs posted by the company
            total_jobs = JobPostings.objects.filter(company=company).count()

            # Total number of applications for the company's jobs
            total_applications = Application.objects.filter(job_posting__company=company).count()

            # Get job posts and their related applications
            job_posts_data = []
            for job in JobPostings.objects.filter(company=company):
                # Get applications for the job post
                applications = Application.objects.filter(job_posting=job)
                job_posts_data.append({
                    'job': job,
                    'applications': applications
                })
        else:
            total_jobs = 0
            total_applications = 0
            job_posts_data = []

        # Render the dashboard with the job posts and application data
        return render(request, 'c_dashboard.html', {
            'total_jobs': total_jobs,
            'total_applications': total_applications,
            'job_posts_data': job_posts_data  # Pass job posts and their applications to the template
        })


# class JobSeekerDashboardView(View):
#    def get(self, request):
#     print("Current User:", request.user, "Is Authenticated:", request.user.is_authenticated)
#     job_postings = JobPostings.objects.all().order_by('-ApplicationDeadline')
#     return render(request, 'jobseekerdashboard.html', {'job_postings': job_postings})
 
   

class CompanyManageJobsView(View):
    def get(self, request):
        return render(request, 'c_managejob.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Notification, UserProfile, JobSeekers, Company

@login_required
def notification_list(request):
    print("🚀 notification_list function is executing!")  # Debuggin
    user = request.user

    # Ensure user has a UserProfile
    user_profile = UserProfile.objects.filter(user=user).first()
    if not user_profile:
        print(f"❌ No UserProfile found for {user.username}")
        return render(request, 'notifications.html', {'notifications': []})
    
    
    notifications = Notification.objects.none()  # Default to empty queryset

    # Get job seeker notifications
    if user_profile.user_type == "seeker":
        job_seeker = JobSeekers.objects.filter(user=user).first()
        if job_seeker:
            notifications = Notification.objects.filter(job_seeker=job_seeker).order_by('-created_at')
            print(f"🔍 Debug: Found {notifications.count()} notifications for Job Seeker {user.username}")
        else:
            print(f"❌ No JobSeeker profile found for {user.username}")
    # Get company notifications
    elif user_profile.user_type == "employer":
        company = Company.objects.filter(user=user).first()
        if company:
            notifications = Notification.objects.filter(company=company).order_by('-created_at')
            print(f"🔍 Debug: Found {notifications.count()} notifications for Employer {user.username}")
        else:
            print(f"❌ No Company profile found for {user.username}")

        print(f"🔍 Debug: Notifications found for {user.username}: {notifications}")  # Debugging
        
    welcome_message = request.session.pop('welcome_message', None)

    return render(
        request, 
        'notifications.html' if user_profile.user_type == "seeker" else 'c_notification.html', 
        {'notifications': notifications, 'welcome_message': f"Welcome, {user.username}!"}
    )

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import JobPostings, Company, Notification, JobSeekers
from .forms import JobPostingForm

@login_required
def post_job(request):
    # try:
    #     company = Company.objects.get(user=request.user)
    # except Company.DoesNotExist:
    #     return redirect('create_company')  # Redirect employer to create a company profile first

    print(f"Logged-in User: {request.user} (ID: {request.user.id})")  # Debugging
    
    company = Company.objects.filter(user=request.user).first()

    if not company:
        print(f"No Company found for user: {request.user}")  # Debugging
        # return redirect('create_company')
    else:
        print(f"Company Found: {company.Name}")  # Debugging

    if request.method == 'POST':
        print(request.POST)  # Debugging the POST data
        
        # Create the form instance with the POST data
        form = JobPostingForm(request.POST)
        
        if form.is_valid():
            print("Form is valid!")  
            new_job = form.save(commit=False)  # Don't save yet
            new_job.company = company  # Assign the company
            new_job.save()  # Save job posting

            # Notify all job seekers
            job_seekers = JobSeekers.objects.all()
            for seeker in job_seekers:
                Notification.objects.create(
                    job_seeker=seeker,
                    message=f"A new job '{new_job.JobTitle}' is available in {new_job.JobLocation}!"
                )
              #  Notify the employer (company) about their job post
            Notification.objects.create(
                company=company,
                message=f"Your job posting '{new_job.JobTitle}' has been successfully listed!",
                is_read=False
            )
            return redirect('company_manage_jobs')  # Redirect after saving
        else:
            print("Form errors:", form.errors)  # Print errors if form is invalid
    else:
        form = JobPostingForm()  # Empty form for GET request

    return render(request, 'c_postjob.html', {'form': form})

@login_required
def manage_jobs_view(request):
    print(f"Logged-in User: {request.user} (ID: {request.user.id})")  # Debugging
    company = Company.objects.filter(user=request.user).first()

    if not company:
        print(f"No Company found for user: {request.user}")  # Debugging
        # return redirect('create_company)
    else:
        print(f"Company Found: {company.Name}")  # Debugging

    jobs = JobPostings.objects.filter(company=company)  # Get only this company's jobs
    total_jobs = jobs.count()  # Count total jobs posted by this company
    return render(request, 'c_managejob.html', {'jobs': jobs, 'total_jobs': total_jobs})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import JobPostings

@login_required
def edit_job(request, job_id):
    # company = get_object_or_404(Company, user=request.user)  # Get the logged-in company
    company = Company.objects.filter(user=request.user).first()
    job = get_object_or_404(JobPostings, id=job_id, company=company)

    if request.method == "POST":
        job.JobTitle = request.POST.get('job_title')
        job.JobLocation = request.POST.get('job_location')
        job.ApplicationDeadline = request.POST.get('job_deadline')
        job.save()
        return redirect('company_manage_jobs')  # Redirect back to Manage Jobs page

    return render(request, 'edit_job.html', {'job': job})

@csrf_exempt
@login_required
def delete_job(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            job_id = data.get('job_id')
            # company = get_object_or_404(Company, user=request.user)  # Get logged-in company
            company = Company.objects.filter(user=request.user).first()
            job = get_object_or_404(JobPostings, id=job_id, company=company)
            job.delete()
            return JsonResponse({'message': 'Job deleted successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


    
class RecommendationsView(View):
    def get(self, request):
        return render(request, 'recommendations.html')  


from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import UserProfile, JobSeekers

@login_required
def jobseeker_profile(request):
    jobseeker_id = request.GET.get('id')  # Get job seeker ID from query parameter

    if jobseeker_id:
        # Employer viewing a job seeker's profile
        jobseeker = get_object_or_404(JobSeekers, id=jobseeker_id)
        user_profile = get_object_or_404(UserProfile, user=jobseeker.user, user_type='seeker')
    else:
        # Job seeker viewing their own profile
        jobseeker = JobSeekers.objects.filter(user=request.user).first()  
        user_profile = UserProfile.objects.filter(user=request.user, user_type='seeker').first()

    return render(request, 'seekerprofile.html', {'user_profile': user_profile, 'jobseeker': jobseeker})


@login_required
def company_profile(request):
    company = Company.objects.filter(user=request.user).first()

    user_profile = get_object_or_404(UserProfile, user=request.user, user_type='employer')

    # Ensure logo exists or set to None if missing
    logo_url = company.logo.url if company.logo else None

    return render(request, 'cprofile.html', {'user_profile': user_profile, 'company': company,'logo_url': logo_url,})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import JobSeekers, UserProfile

@login_required
def employer_view_jobseeker_profile(request, jobseeker_id):
    jobseeker = get_object_or_404(JobSeekers, id=jobseeker_id)
    user_profile = get_object_or_404(UserProfile, user=jobseeker.user, user_type='seeker')

    return render(request, 'employer_view_seeker_profile.html', {'user_profile': user_profile, 'jobseeker': jobseeker})

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import JobSeekers, UserProfile

@login_required
def update_jobseeker_profile(request):
    if request.method == 'POST':
        user = request.user
        jobseeker = get_object_or_404(JobSeekers, user=user)
        user_profile = get_object_or_404(UserProfile, user=user, user_type='seeker')

        # Update user details
        jobseeker.full_name = request.POST.get('full_name', jobseeker.full_name)
        # user_profile.full_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        # jobseeker.phone = request.POST.get('phone')
        # jobseeker.location = request.POST.get('location')
        jobseeker.phone = request.POST.get('phone', jobseeker.phone)
        jobseeker.location = request.POST.get('location', jobseeker.location)
        jobseeker.interpersonal_skills = request.POST.get('interpersonal_skills', jobseeker.interpersonal_skills)
        jobseeker.technical_skills = request.POST.get('technical_skills', jobseeker.technical_skills)
        jobseeker.experience = request.POST.get('experience', jobseeker.experience)
        jobseeker.education = request.POST.get('education', jobseeker.education)

        # Save changes
        user_profile.save()
        user.save()
        jobseeker.save()

        return JsonResponse({'message': 'Profile updated successfully'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from .utils import verify_token

def verify_email(request, token):
    email = verify_token(token)
    
    if email is None:
        messages.error(request, "Invalid or expired verification link.")
        return redirect("login")

    try:
        user = User.objects.get(email=email)
        user.is_active = True  # Activate user account
        user.save()
        messages.success(request, "Your email has been verified. You can now log in.")
        return redirect("login")
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("register")


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str

# def verify_email(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = get_user_model().objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
#         user = None

#     if user is not None:
#         if user.is_active:
#             return redirect('/login/?message=Your account is already verified. Please log in.')

#         if default_token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()
#             return redirect('/login/?message=Your email has been verified. You can now log in.')

#     return redirect('/login/?message=Invalid or expired verification link.')

# def verify_email(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None:
#         if user.is_active:
#             return redirect('/login/?message=Your account is already verified. Please log in.')

#         if default_token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()
#             print("DEBUG: User activated successfully!")  # Debugging
#             return redirect('/login/?message=Your email has been verified. You can now log in.')

#     print("DEBUG: Invalid or expired token!")  # Debugging
#     return redirect('/login/?message=Invalid or expired verification link.')

def verify_email(request, uidb64, token):
    from django.utils.encoding import force_str
    from django.utils.http import urlsafe_base64_decode
    from django.contrib.auth.models import User
    from django.contrib.auth.tokens import default_token_generator
    from django.shortcuts import redirect
    from django.contrib import messages

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(f"DEBUG: Decoded UID - {uid}")  # Debugging

        user = User.objects.get(pk=uid)
        print(f"DEBUG: Retrieved User - {user.email}, is_active: {user.is_active}")  # Debugging

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        print("DEBUG: No user found for this UID!")  # Debugging
        user = None

    if user is not None:
        if user.is_active:
            messages.success(request, "Your account is already verified. Please log in.")
            return redirect('/login/')

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            user.refresh_from_db()  

            print(f"DEBUG: User activated - {user.email}, is_active: {user.is_active}")  # Debugging

            messages.success(request, "Your email has been verified. You can now log in.")
            return redirect('/login/')
    
    print("DEBUG: Invalid or expired token!")
    messages.error(request, "Invalid or expired verification link.")
    return redirect('/login/')

from django.shortcuts import render
from django.http import JsonResponse
from .models import JobPostings

def search_jobs(request):
    query = request.GET.get('q', '')  # Get search query from request
    jobs = JobPostings.objects.all()  # Start with all jobs

    if query:
        jobs = jobs.filter(
            JobTitle__icontains=query  # Filter jobs by title (case-insensitive)
        )  # Use JobTitle with the correct casing

    job_data = [
        {
            "id": job.id,
            "title": job.JobTitle,  # Use JobTitle with the correct casing
            "company": job.company.Name if job.company else "Not Available",  # Ensure 'Name' is the correct field in the Company model
            "location": job.JobLocation,  # Use JobLocation with the correct casing
            "description": job.JobDescription,  # Use JobDescription with the correct casing
            "deadline": job.ApplicationDeadline.strftime("%Y-%m-%d"),  # Use ApplicationDeadline with the correct casing
        }
        for job in jobs
    ]

    return JsonResponse({"jobs": job_data})  # Return filtered jobs as JSON

#autocomplete
from django.http import JsonResponse
from .models import JobPostings

def job_search_suggestions(request):
    query = request.GET.get('query', '')
    if query:
        # Case-insensitive search for job titles that contain the query
        jobs = JobPostings.objects.filter(JobTitle__icontains=query)
        # Collect job titles as suggestions
        suggestions = [job.JobTitle for job in jobs]
    else:
        suggestions = []

    # Return the suggestions as a JSON response
    return JsonResponse(suggestions, safe=False)

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.shortcuts import render

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
 
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification, UserProfile, JobSeekers, Application
from django.core.exceptions import ObjectDoesNotExist

@login_required
def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)

    # Determine if the user is an employer or job seeker
    user_profile = UserProfile.objects.filter(user=request.user).first()
    base_template = "jobseeker_base.html" if user_profile and user_profile.user_type == "seeker" else "base.html"

    # Safely handle missing related objects
    job_seeker = getattr(notification, 'job_seeker', None)
    
    try:
        application = notification.application  # Try to get application from notification
    except ObjectDoesNotExist:
        application = None  # If no application is linked, set it to None

    # Debugging logs
    print(f"DEBUG: Notification ID: {notification_id}")
    print(f"DEBUG: Job Seeker: {job_seeker}")
    print(f"DEBUG: Application: {application}")

    # If job seeker and application are not set, try fetching them from related ids
    if not job_seeker and hasattr(notification, 'job_seeker_id'):
        job_seeker = JobSeekers.objects.filter(id=notification.job_seeker_id).first()
    
    if not application and hasattr(notification, 'application_id'):
        application = Application.objects.filter(id=notification.application_id).first()

    # Debug logs for fetched data
    print(f"DEBUG: Fetched Job Seeker: {job_seeker}")  
    print(f"DEBUG: Fetched Application: {application}")  

    if not notification.is_read:
        notification.is_read = True
        notification.save()
    
    # Render the template with the necessary context
    return render(request, 'notification_detail.html', {
        'notification': notification,
        'job_seeker': job_seeker,
        'application': application,
        'base_template': base_template
    })

@login_required
def dismiss_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, 
                                    job_seeker=request.user.jobseekers if hasattr(request.user, 'jobseekers') else None, 
                                    company=request.user.company if hasattr(request.user, 'company') else None)
    
    notification.delete()
    return JsonResponse({"success": True})


from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from core.models import Application

@csrf_exempt
def update_application_status(request, application_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            status = data.get("status")

            application = Application.objects.get(id=application_id)
            application.status = status
            application.save()

            # Send email only when accepted
            if status == "Accepted":
                send_mail(
                    subject="Congratulations! You've been accepted",
                    message=f"Dear {application.job_seeker.full_name},\n\n"
                            f"Congratulations! You have been selected for an interview for the job: {application.job_posting.JobTitle}.\n\n"
                            f"Best Regards,\n{application.job_posting.company.Name}",
                    from_email=application.job_posting.company.CompanyEmail,
                    recipient_list=[application.job_seeker.user.email],
                    fail_silently=False,
                )

            if status == "Rejected":
                send_mail(
                    subject="Job Application Update",
                    message=f"Dear {application.job_seeker.full_name},\n\n"
                            f"Unfortunately, your application for the job: {application.job_posting.title} has been rejected.\n\n"
                            f"Keep applying for other jobs. We wish you the best!\n\n"
                            f"Best Regards,\n{application.job_posting.company.name}",
                    from_email=application.job_posting.company.CompanyEmail,
                    recipient_list=[application.job_seeker.user.email],
                    fail_silently=False,
                )


            return JsonResponse({"success": True, "message": f"Application status updated to {status}"})

        except Application.DoesNotExist:
            return JsonResponse({"success": False, "message": "Application not found"}, status=404)

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import JobSeekers

@login_required
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        job_seeker = JobSeekers.objects.get(user=request.user)
        job_seeker.profile_picture = request.FILES['profile_picture']
        job_seeker.save()
        return JsonResponse({'profile_picture_url': job_seeker.profile_picture.url})
    return JsonResponse({'error': 'No file uploaded'}, status=400)


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Company, UserProfile

@login_required
def update_company_profile(request):
    
    if request.method == 'POST':
        user = request.user
        company = get_object_or_404(Company, user=user)

        # Update fields
        company.Name = request.POST.get('company_name', company.Name)
        company.CompanyEmail = request.POST.get('company_email', company.CompanyEmail)
        company.CompanyPhone = request.POST.get('company_phone', company.CompanyPhone)
        company.CompanyAddress = request.POST.get('company_address', company.CompanyAddress)
        company.CompanyIndustry = request.POST.get('company_industry', company.CompanyIndustry)

        company.save()
        return JsonResponse({'message': 'Company profile updated successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def upload_company_logo(request):
    if request.method == 'POST' and request.FILES.get('company_logo'):
        company = get_object_or_404(Company, user=request.user)
        company.logo = request.FILES['company_logo']
        company.save()
        return JsonResponse({'logo_url': company.logo.url})
    return JsonResponse({'error': 'No file uploaded'}, status=400)

@login_required
def update_contact_profile(request):
    if request.method == "POST":
        company_id = request.POST.get('company_id')  # Assuming CompanyID is sent in POST request
        contact_name = request.POST.get('contact_name')
        contact_email = request.POST.get('contact_email')
        contact_phone = request.POST.get('contact_phone')

        # Fetch company object by CompanyID (or user association)
        try:
            company = Company.objects.get(CompanyID=company_id)
        except Company.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Company not found"})

        # Update the contact person profile
        company.ContactPersonName = contact_name
        company.ContactPersonEmail = contact_email
        company.ContactPersonPhone = contact_phone
        company.save()

        return JsonResponse({"status": "success", "message": "Contact person profile updated successfully!"})




from django.shortcuts import render
from .models import JobSeekers
from .recommendation import recommend_jobs

def job_recommendations(request):
    user = request.user
    job_seeker = JobSeekers.objects.filter(user=user).first()

    if not job_seeker:
        return render(request, 'no_profile.html')

    recommendations = recommend_jobs(job_seeker.id)
    return render(request, 'recommendations.html', {'recommended_jobs': recommendations})


def match_skills(job_requirements, seeker_skills):
    """
    Match skills between job requirements and job seeker's skills.
    """
    job_skills = [skill.strip().lower() for skill in job_requirements.split(',')]
    seeker_skills = [skill.strip().lower() for skill in seeker_skills.split(',')]
    common_skills = set(job_skills).intersection(set(seeker_skills))
    return len(common_skills) * 10  # Reward 10 points for each matching skill

def match_experience(job_experience, seeker_experience):
    """
    Match experience level between job requirements and job seeker's experience.
    """
    # Example: Simple matching based on keywords
    if "entry" in job_experience.lower() and "entry" in seeker_experience.lower():
        return 10
    elif "mid" in job_experience.lower() and "mid" in seeker_experience.lower():
        return 20
    elif "senior" in job_experience.lower() and "senior" in seeker_experience.lower():
        return 30
    return 0

def match_education(job_education, seeker_education):
    """
    Match education level between job requirements and job seeker's education.
    """
    # Example: Simple matching based on keywords
    if "bachelor" in job_education.lower() and "bachelor" in seeker_education.lower():
        return 10
    elif "master" in job_education.lower() and "master" in seeker_education.lower():
        return 20
    elif "phd" in job_education.lower() and "phd" in seeker_education.lower():
        return 30
    return 0