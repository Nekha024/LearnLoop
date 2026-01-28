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
    