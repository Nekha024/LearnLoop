from django.contrib import admin
from .models import CodingQuestion, UserCodingProfile

@admin.register(CodingQuestion)
class CodingQuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'time_limit_seconds')

@admin.register(UserCodingProfile)
class UserCodingProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'attempts', 'skill_rating')



from django.contrib import admin
from .models import CareerAssessment


@admin.register(CareerAssessment)
class CareerAssessmentAdmin(admin.ModelAdmin):
    list_display = ["id", "top_career_1", "top_career_2", "top_career_3", "score_1", "score_2", "score_3", "created_at", "ip_address"]
    list_filter = ["top_career_1", "created_at"]
    search_fields = ["top_career_1", "top_career_2", "top_career_3", "ip_address"]
    readonly_fields = ["answers", "raw_prediction", "created_at", "ip_address"]
    ordering = ["-created_at"]

    fieldsets = (
        ("Prediction Results", {
            "fields": ("top_career_1", "score_1", "top_career_2", "score_2", "top_career_3", "score_3")
        }),
        ("Session Info", {
            "fields": ("user", "session_key", "ip_address", "created_at")
        }),
        ("Raw Data", {
            "classes": ("collapse",),
            "fields": ("answers", "raw_prediction"),
        }),
    )
