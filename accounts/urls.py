from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth_view, name='auth'),  # User login and signup
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Mentor authentication (login/signup)
    path('mentor/auth/', views.mentor_auth_view, name='mentor_auth'),
    
    # ❌ REMOVE THIS LINE - mentor dashboard is now in mentor/urls.py
    # path('mentor/dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
    
    # Admin mentor approval
    path('dashboard/admin/approve/<int:mentor_id>/', views.approve_mentor, name='approve_mentor'),
    # Delete mentor URL
    path('dashboard/admin/delete/<int:mentor_id>/', views.delete_mentor, name='delete_mentor'),
    path('logout/',views.log_out,name='logout')
]
