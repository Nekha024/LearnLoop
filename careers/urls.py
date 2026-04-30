from django.urls import path
from . import views

app_name = 'careers'
urlpatterns = [
    path('', views.careers_view, name='roads'), #Careers main page
    # path('predict/', views.career_prediction_view, name='careerpred'), #Career prediction
    
    path('arena/', views.code_arena, name='codearena'), #Coding arena main page
    
    # This is the internal API path the JavaScript calls to get AI evaluation
    path('evaluate/', views.evaluate_code, name='evaluate_code'),


    path("assessment/", views.assessment_view, name="assessment"),
    path("predict/", views.predict_view, name="predict"),
    path("roadmap/<slug:role_slug>/", views.roadmap_view, name="roadmap"),

]