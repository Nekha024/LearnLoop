from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('mentor', 'Mentor'),
        ('Admin', 'Admin'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )
    phone_regex = RegexValidator(
    regex=r'^[9876]\d{9}$',
    message="Phone number must be a 10-digit number and start with 9, 8, 7, or 6."
    )
    phone_number = models.CharField(
        max_length=10, 
        blank=True, 
        null=True, 
        validators=[phone_regex],
        unique=True,
        help_text='Enter 10 digit phone number'
    )
        
    previous_experience = models.BooleanField(blank=True, null=True,verbose_name="Previous Experience")

    is_approved=models.BooleanField(default=False)
    
    
    #Mentor related fields
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=False,
        null=False
    )
        
    profile_photo = models.ImageField(upload_to='mentor_photos/', blank=False, null=True)

    # Professional info
    profession = models.CharField(max_length=100, blank=False, null=True)
    experience_years = models.PositiveIntegerField(
        null=True,
        blank=False,

    )
    expertise = models.CharField(
        blank=False,
        null=True,
        max_length=100,
        
    )  
    bio = models.CharField(
        blank=False,
        null=True,
    )

    linkedin = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)

    # Mentorship availability
    available_days = models.JSONField(default=list)  # ["mon", "wed", "fri"]
    available_from = models.TimeField(default="09:00")
    available_to = models.TimeField(default="17:00")

    session_duration = models.CharField(
        max_length=10,
        choices=[
            ('30', '30 Minutes'),
            ('60', '60 Minutes'),
        ],null=True, blank=False
    )

    intro_video = models.FileField(upload_to="mentor_videos/", blank=True, null=True)

    # Auto timestamp
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True
    )
    def __str__(self):
        return self.username