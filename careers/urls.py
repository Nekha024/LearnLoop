from django.urls import path
from . import views

urlpatterns = [
    path('', views.careers_view, name='careers'), #Careers main page
    path('predict/', views.career_predict, name='career_predict'), #Career prediction
    
    path('arena/', views.code_arena, name='codearena'), #Coding arena main page
    
    # This is the internal API path the JavaScript calls to get AI evaluation
    path('evaluate/', views.evaluate_code, name='evaluate_code')
]