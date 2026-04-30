from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser


# EXISTING MODEL - KEPT AS IS
class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    mentor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mentor_appointments')
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_created=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} -> {self.mentor} on {self.date}"


# NEW MODELS FOR MENTOR DASHBOARD
class MentorProfile(models.Model):
    """Extended profile for mentors - stores additional mentor-specific data"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='mentor_profile'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Professional bio (max 500 characters)"
    )
    expertise = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Comma-separated skills (e.g., Python, Django, React)"
    )
    fee_30min = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        help_text="Fee (in Rupee) for 30-minute session"
    )
    fee_60min = models.IntegerField(
        default=20,
        validators=[MinValueValidator(0), MaxValueValidator(2000)],
        help_text="Fee (in Rupee) for 60-minute session"
    )
    total_sessions = models.IntegerField(default=0)
    total_earnings = models.IntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mentor Profile"
        verbose_name_plural = "Mentor Profiles"

    def __str__(self):
        return f"Mentor Profile: {self.user.username}"


class AvailabilitySlot(models.Model):
    """Weekly recurring availability slots for mentors"""
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    mentor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='mentor_availability_slots',
        limit_choices_to={'role': 'mentor'}
    )
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Availability Slot"
        verbose_name_plural = "Availability Slots"
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.mentor.username} - {self.day_of_week}: {self.start_time} to {self.end_time}"


class MentorshipSession(models.Model):
    """Individual mentorship session bookings - Enhanced version of Appointment"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    DURATION_CHOICES = [
        (30, '30 minutes'),
        (60, '60 minutes'),
    ]
    
    mentor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='mentor_sessions',
        limit_choices_to={'role': 'mentor'}
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='student_sessions'
        # ✅ REMOVED limit_choices_to - allows any user to book
    )
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    duration = models.IntegerField(choices=DURATION_CHOICES, default=30)
    fee_amount = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    topic = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)  # ✅ Changed from 'note' to 'notes'
    meeting_link = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Mentorship Session"
        verbose_name_plural = "Mentorship Sessions"
        ordering = ['-scheduled_date', '-scheduled_time']

    def __str__(self):
        return f"{self.student.username} → {self.mentor.username} on {self.scheduled_date}"


class ContentContribution(models.Model):
    """Blog posts and tutorials contributed by mentors"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('published', 'Published'),
        ('rejected', 'Rejected'),
    ]
    
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='mentor_contributions'
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    images=models.ImageField(upload_to='contributions/images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    reward_amount = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Content Contribution"
        verbose_name_plural = "Content Contributions"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author.username}"
