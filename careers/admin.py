from django.contrib import admin
from .models import CodingQuestion, UserCodingProfile

@admin.register(CodingQuestion)
class CodingQuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'time_limit_seconds')

@admin.register(UserCodingProfile)
class UserCodingProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'attempts', 'skill_rating')