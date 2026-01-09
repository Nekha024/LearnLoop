from django.contrib import admin
from .models import Appointment, MentorProfile, AvailabilitySlot, MentorshipSession, ContentContribution


# EXISTING APPOINTMENT ADMIN
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'mentor', 'date', 'time', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['user__username', 'mentor__username']


# NEW ADMIN CLASSES
@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'fee_30min', 'fee_60min', 'total_sessions', 'total_earnings', 'rating', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'expertise']
    readonly_fields = ['created_at', 'updated_at', 'total_sessions', 'total_earnings']
    
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('bio', 'expertise')
        }),
        ('Pricing', {
            'fields': ('fee_30min', 'fee_60min')
        }),
        ('Statistics', {
            'fields': ('total_sessions', 'total_earnings', 'rating')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'day_of_week', 'start_time', 'end_time', 'is_active']
    list_filter = ['day_of_week', 'is_active', 'created_at']
    search_fields = ['mentor__username']


@admin.register(MentorshipSession)
class MentorshipSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'mentor', 'student', 'scheduled_date', 'scheduled_time', 'duration', 'status', 'token_fee']
    list_filter = ['status', 'duration', 'scheduled_date', 'created_at']
    search_fields = ['mentor__username', 'student__username', 'topic']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    
    fieldsets = (
        ('Participants', {
            'fields': ('mentor', 'student')
        }),
        ('Schedule', {
            'fields': ('scheduled_date', 'scheduled_time', 'duration')
        }),
        ('Details', {
            'fields': ('topic', 'notes', 'meeting_link', 'token_fee')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at', 'completed_at')
        }),
    )


@admin.register(ContentContribution)
class ContentContributionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'token_reward', 'views_count', 'created_at', 'published_at']
    list_filter = ['status', 'created_at', 'published_at']
    search_fields = ['title', 'author__username', 'body']
    readonly_fields = ['created_at', 'updated_at', 'published_at', 'views_count']
    
    fieldsets = (
        ('Content', {
            'fields': ('author', 'title', 'body')
        }),
        ('Status & Rewards', {
            'fields': ('status', 'token_reward', 'views_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at')
        }),
    )
