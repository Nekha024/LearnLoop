from django.urls import path
from . import views

urlpatterns = [
    path('room/<int:session_id>/', views.chat_room, name='chat_room'),
    path('send/<int:session_id>/', views.send_message, name='send_message'),
]
