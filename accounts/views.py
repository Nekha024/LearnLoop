from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.http import HttpResponseForbidden
from django.views.decorators.cache import never_cache
from .models import CustomUser
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout


def auth_view(request):
    signup_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm(request)

    if request.method == 'POST':
        if 'signup_submit' in request.POST:
            signup_form = CustomUserCreationForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                messages.success(request, "Account created successfully! You can now log in.")
                signup_form = CustomUserCreationForm()
            else:
                messages.error(request, "Signup failed. Please fix the errors below.")

        elif 'login_submit' in request.POST:
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()  
                if user:
                    login(request, user)
                    role = getattr(user, 'role', 'user')  
                    if user.is_superuser:
                        return redirect('admin_dashboard')
                    elif role == 'mentor':
                        # CHANGED: Redirect to mentor app dashboard
                        return redirect('mentor_dashboard')
                    else:
                        return redirect('user_dashboard')
                else:
                    messages.error(request, "Invalid username or password.")

    return render(request, 'registration/login.html', {
        'signup_form': signup_form,
        'login_form': login_form
    })


def mentor_auth_view(request):
    mentor_signup = MentorCreationForm()
    mentor_login = MentorLoginForm(request)

    if request.method == 'POST':
        if 'mentor_submit' in request.POST:
            mentor_signup = MentorCreationForm(request.POST or None, request.FILES)
            if mentor_signup.is_valid():
                user = mentor_signup.save(commit=False)
                user.role = 'mentor'
                user.is_approved = False  
                user.save()
                messages.success(request, "Mentor account created! Wait for admin approval before logging in.")
                mentor_signup = MentorCreationForm()               
            else:
                messages.error(request, "Signup failed. Please fix the errors below.")

        elif 'mlogin_submit' in request.POST:
            mentor_login = MentorLoginForm(request, data=request.POST)
            if mentor_login.is_valid():
                user = mentor_login.get_user()
                if user:
                    role = getattr(user, 'role', 'user')
                    if user.is_superuser:
                        login(request, user)
                        return redirect('admin_dashboard')
                    elif role == 'mentor':
                        if not user.is_approved:
                            messages.error(request, "Your account is awaiting admin approval. Try Signing in after 15-30 mins. Thank you")
                            return redirect('mentor_auth')
                        login(request, user)
                        # CHANGED: Redirect to mentor app dashboard
                        return redirect('mentor_dashboard')
                    else:
                        messages.error(request, "This account is not a Mentor account. Please use the general login.")
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'registration/mentor_registration.html', {
        'mentor_signup': mentor_signup,
        'mentor_login': mentor_login
    })


@never_cache
@login_required
def user_dashboard(request):
    return render(request, 'dashboard/user_dashboard.html')


# REMOVED OLD MENTOR_DASHBOARD VIEW - Now handled by mentor/views.py


@never_cache
@login_required
def admin_dashboard(request):
    if request.user.is_superuser == False:
        return HttpResponseForbidden("Not allowed here.")
    
    all_mentors = CustomUser.objects.filter(role='mentor')
    users = CustomUser.objects.filter(role='user')
    
    context = {
        'mentors': all_mentors.filter(is_approved=False),
        'approved_mentors_count': all_mentors.filter(is_approved=True).count(),
        'total_mentors_count': all_mentors.count(),
        'all_mentors': all_mentors,
        'users': users,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


def approve_mentor(request, mentor_id):
    if request.user.is_superuser == False:
        return HttpResponseForbidden("Not allowed")
    mentor = get_object_or_404(CustomUser, id=mentor_id, role='mentor')
    mentor.is_approved = True
    mentor.save()
    messages.success(request, f"{mentor.username} has been approved!")
    return redirect('admin_dashboard')


@login_required
def delete_mentor(request, mentor_id):
    # Only allow Admin role
    if request.user.is_superuser == False:
        return HttpResponseForbidden("You are not allowed here.")

    mentor = get_object_or_404(CustomUser, id=mentor_id, role='mentor')
    mentor_username = mentor.username
    mentor.delete()
    messages.success(request, f"Mentor '{mentor_username}' has been deleted successfully!")
    return redirect('admin_dashboard')

def log_out(request):
    logout(request)
    return redirect('auth')
