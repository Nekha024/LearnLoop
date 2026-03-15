from django.apps import AppConfig


class CareersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'careers'


from django.apps import AppConfig


class CareerPredictorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "career_predictor"
    verbose_name = "IT Career Predictor"
