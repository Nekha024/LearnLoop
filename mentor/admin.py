from django.contrib import admin
from .models import Appointment, MentorProfile, AvailabilitySlot, MentorshipSession, ContentContribution
from django.utils.html import format_html


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
    list_display = ['id', 'mentor', 'student', 'scheduled_date', 'scheduled_time', 'duration', 'status', 'fee_amount']
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
            'fields': ('topic', 'notes', 'meeting_link', 'fee_amount')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at', 'completed_at')
        }),
    )


# @admin.register(ContentContribution)
# class ContentContributionAdmin(admin.ModelAdmin):
#     list_display = ['title', 'author', 'status', 'token_reward', 'views_count', 'created_at', 'published_at']
#     list_filter = ['status', 'created_at', 'published_at']
#     search_fields = ['title', 'author__username', 'body']
#     readonly_fields = ['created_at', 'updated_at', 'published_at', 'views_count']
    
#     fieldsets = (
#         ('Content', {
#             'fields': ('author', 'title', 'body')
#         }),
#         ('Status & Rewards', {
#             'fields': ('status', 'token_reward', 'views_count')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at', 'published_at')
#         }),
#     )


@admin.register(ContentContribution)
class ContentContributionAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'status',
        'reward_amount', 'views_count',
        'created_at', 'published_at'
    ]

    list_filter = ['status', 'created_at', 'published_at']
    search_fields = ['title', 'author__username', 'body']

    readonly_fields = [
        'created_at', 'updated_at',
        'published_at', 'views_count',
        'images_preview'   # 👈 renamed
    ]

    fieldsets = (
        ('Content', {
            'fields': ('author', 'title', 'body', 'images')  # 👈 renamed
        }),
        ('Status & Rewards', {
            'fields': ('status', 'reward_amount', 'views_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at')
        }),
        ('Preview', {
            'fields': ('images_preview',),
        }),
    )

    def images_preview(self, obj):
        if obj.images:
            return format_html(
                '<img src="{}" style="max-height: 200px; border-radius: 6px;" />',
                obj.images.url
            )
        return "No Image"

    images_preview.short_description = "Image Preview"