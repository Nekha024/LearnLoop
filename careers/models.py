from django.db import models
from django.conf import settings

# Create your models here.
class CodingQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    # Added default='Easy' to fix the Migration error
    difficulty = models.CharField(
        max_length=50, 
        choices=DIFFICULTY_CHOICES, 
        default='Easy' 
    )
    # The code the user starts with (e.g., "def solution(n):")
    template_code = models.TextField(default="def solution():\n    # Write your code here\n    pass")
    time_limit_seconds = models.IntegerField(default=60)

    def __str__(self):
        return self.title

class UserCodingProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_score = models.FloatField(default=0.0)
    attempts = models.IntegerField(default=0)

    @property
    def skill_rating(self):
        if self.attempts == 0: return "Not Rated"
        avg = self.total_score / self.attempts
        if avg >= 80: return "Good"
        elif avg >= 50: return "Average"
        return "Low"


from django.db import models
from django.contrib.auth.models import User
import json


class CareerAssessment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=100, blank=True)
    answers = models.JSONField()
    top_career_1 = models.CharField(max_length=100, blank=True)
    top_career_2 = models.CharField(max_length=100, blank=True)
    top_career_3 = models.CharField(max_length=100, blank=True)
    score_1 = models.IntegerField(default=0)
    score_2 = models.IntegerField(default=0)
    score_3 = models.IntegerField(default=0)
    raw_prediction = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Career Assessment"
        verbose_name_plural = "Career Assessments"

    def __str__(self):
        return f"Assessment #{self.id} - {self.top_career_1} ({self.created_at.strftime('%Y-%m-%d')})"

    def get_answers_display(self):
        return json.dumps(self.answers, indent=2)
