from django.urls import path
from . import views

urlpatterns = [
    # Browse & Book Mentors (Student/User Side)
    path('browse/', views.mentor_list, name='mentor_list'),
    path('detail/<int:id>/', views.mentor_detail, name='mentor_detail'),
    path('book/<int:id>/', views.book_session, name='book_session'),  # UPDATED
    
    # User Session Management
    path('my-sessions/', views.user_sessions, name='user_sessions'),
    path('session/cancel/<int:session_id>/', views.cancel_session, name='cancel_session'),
    
    # Mentor Dashboard (main view)
    path('dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
    # path('dashboard/profile/', views.mentor_profile, name='mentor_profile_setup'),
        path('dashboard/profile/', views.mentor_profile, name='mentor_profile_setup'),

    path('dashboard/content', views.mentor_content, name='mentor_content'),
    # Availability Management (Mentor)
    path('availability/add/', views.add_availability_slot, name='add_availability'),
    path('availability/remove/<int:slot_id>/', views.remove_availability_slot, name='remove_availability'),
    
    # Session Management (Mentor)
    path('session/accept/<int:session_id>/', views.accept_session, name='accept_session'),
    path('session/decline/<int:session_id>/', views.decline_session, name='decline_session'),
    path('session/complete/<int:session_id>/', views.complete_session, name='complete_session'),
    
    # Content Contribution (Mentor)
    path('content/submit/', views.submit_content, name='submit_content'),
    path('content/edit/<int:content_id>/', views.edit_content, name='edit_content'),
    path('content/delete/<int:content_id>/', views.delete_content, name='delete_content'),

    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:content_id>/', views.blog_detail, name='blog_detail'),
    
]
