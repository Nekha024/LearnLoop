from django.urls import path
from . import views

urlpatterns = [
    path('', views.careers_view, name='careers'), #Careers main page
    path('predict/', views.career_predict, name='career_predict'), #Career prediction
]