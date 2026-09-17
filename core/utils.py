from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)

email_verification_token = EmailVerificationTokenGenerator()


from django.core import signing

def generate_verification_token(email):
    return signing.dumps(email)  # Securely sign the email

def verify_token(token, expiration=3600):  # 1-hour expiration
    try:
        email = signing.loads(token, max_age=expiration)  # Decode token
        return email
    except signing.BadSignature:
        return None  # Invalid token
    except signing.SignatureExpired:
        return None  # Expired token
    




import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Tokenize
    words = text.split()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(words)


# jobs/recommendation_utils.py
def combine_features(job_seeker):
    return (
        job_seeker.technical_skills + ' ' +
        job_seeker.interpersonal_skills + ' ' +
        job_seeker.experience + ' ' +
        job_seeker.education
    )

def prepare_job_data(job_posting):
    return (
        job_posting.JobTitle + ' ' +
        job_posting.JobDescription + ' ' +
        job_posting.JobRequirements + ' ' +
        job_posting.JobType
    )


# jobs/recommendation_utils.py
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Prefetch

class JobRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.job_vectors = None
        self.jobs = None
        
    def train(self):
        # Get all active job postings
        self.jobs = JobPostings.objects.filter(
            ApplicationDeadline__gte=timezone.now()
        ).prefetch_related('company')
        
        # Prepare job data
        job_texts = [prepare_job_data(job) for job in self.jobs]
        preprocessed_jobs = [preprocess_text(text) for text in job_texts]
        
        # Fit TF-IDF vectorizer
        self.job_vectors = self.vectorizer.fit_transform(preprocessed_jobs)
        
    def recommend_jobs(self, job_seeker, top_n=5):
        # Prepare seeker data
        seeker_text = combine_features(job_seeker)
        preprocessed_seeker = preprocess_text(seeker_text)
        
        # Transform to TF-IDF
        seeker_vector = self.vectorizer.transform([preprocessed_seeker])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(seeker_vector, self.job_vectors)
        
        # Get top N indices
        similar_indices = similarities.argsort()[0][-top_n:][::-1]
        
        # Return recommended jobs
        return [self.jobs[i] for i in similar_indices]