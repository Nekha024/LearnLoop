from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils import timezone
from django.db.models import Q
from httpcore import request
from accounts.models import CustomUser
from django.views.decorators.http import require_POST
from .models import (
    Appointment, 
    MentorProfile, 
    AvailabilitySlot, 
    MentorshipSession, 
    ContentContribution
)


# ==================== EXISTING VIEWS ====================

def mentor_list(request):
    """Browse all approved mentors"""
    mentors = CustomUser.objects.filter(role='mentor', is_approved=True)
    
    mentors_with_profiles = []
    for mentor in mentors:
        try:
            profile = MentorProfile.objects.get(user=mentor)
        except MentorProfile.DoesNotExist:
            profile = None
        
        mentors_with_profiles.append({
            'mentor': mentor,
            'profile': profile
        })
    
    context = {
        'mentors': mentors_with_profiles
    }
    return render(request, 'mentor_browse.html', context)


def mentor_detail(request, id):
    """View mentor profile details"""
    mentor = get_object_or_404(CustomUser, id=id, role='mentor')
    
    # Get mentor profile if exists
    try:
        mentor_profile = MentorProfile.objects.get(user=mentor)
    except MentorProfile.DoesNotExist:
        mentor_profile = None
    
    # Get availability slots
    availability_slots = AvailabilitySlot.objects.filter(
        mentor=mentor,
        is_active=True
    ).order_by('day_of_week', 'start_time')
    
    # Get user's sessions with this mentor (if logged in)
    user_sessions = None
    if request.user.is_authenticated:
        user_sessions = MentorshipSession.objects.filter(
            mentor=mentor,
            student=request.user
        ).order_by('-scheduled_date', '-scheduled_time')[:5]
    
    # Pre-split expertise string into a list for the template
    raw_expertise = (mentor_profile.expertise if mentor_profile and mentor_profile.expertise else mentor.expertise) or ''
    expertise_tags = [tag.strip() for tag in raw_expertise.split(',') if tag.strip()]

    context = {
        'mentor': mentor,
        'mentor_profile': mentor_profile,
        'availability_slots': availability_slots,
        'user_sessions': user_sessions,
        'expertise_tags': expertise_tags,
    }
    return render(request, 'mentor_detail.html', context)


@login_required
def book_appointment(request, id):
    """Book appointment with mentor (old system - for backward compatibility)"""
    mentor = get_object_or_404(CustomUser, id=id, role='mentor')

    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')

        Appointment.objects.create(
            user=request.user,
            mentor=mentor,
            date=date,
            time=time,
            note=note
        )
        messages.success(request, "✅ Appointment booked successfully!")
        return redirect('mentor_detail', id=mentor.id)

    return render(request, 'book_appointments.html', {'mentor': mentor})


# ==================== MENTOR DASHBOARD VIEWS ====================

@never_cache
@login_required
def mentor_dashboard(request):
    """Main mentor dashboard view with profile management"""
    
    # Check if user is mentor
    if request.user.role != 'mentor':
        messages.error(request, "⛔ This page is only accessible to mentors.")
        return redirect('home')
    
    if not request.user.is_approved:
        messages.error(request, "⏳ You must be approved by admin to access the mentor dashboard.")
        return redirect('home')
    
    # # Get or create mentor profile
    # mentor_profile, created = MentorProfile.objects.get_or_create(
    #     user=request.user,
    #     defaults={
    #         'bio': getattr(request.user, 'bio', ''),
    #         'expertise': getattr(request.user, 'expertise', ''),
    #         'fee_30min': 10,
    #         'fee_60min': 20,
    #     }
    # )
    
    # # Handle profile update form submission
    # if request.method == 'POST':
    #     bio = request.POST.get('bio', '').strip()
    #     skills = request.POST.get('skills', '').strip()
    #     fee_30m = request.POST.get('fee_30m', 10)
    #     fee_60m = request.POST.get('fee_60m', 20)
        
    #     if len(bio) > 500:
    #         messages.error(request, "❌ Bio must be 500 characters or less.")
    #         return redirect('mentor_dashboard')
        
    #     try:
    #         mentor_profile.bio = bio
    #         mentor_profile.expertise = skills
    #         mentor_profile.fee_30min = int(fee_30m) if fee_30m else 10
    #         mentor_profile.fee_60min = int(fee_60m) if fee_60m else 20
    #         mentor_profile.save()
            
    #         if hasattr(request.user, 'bio'):
    #             request.user.bio = bio
    #         if hasattr(request.user, 'expertise'):
    #             request.user.expertise = skills
    #         request.user.save()
            
    #         messages.success(request, "✅ Profile updated successfully!")
    #         return redirect('mentor_dashboard')
            
    #     except ValueError as e:
    #         messages.error(request, "❌ Invalid fee values. Please enter valid numbers.")
    #         return redirect('mentor_dashboard')
    #     except Exception as e:
    #         messages.error(request, f"❌ Error updating profile: {str(e)}")
    #         return redirect('mentor_dashboard')
    
    # Get pending session requests
    pending_sessions = MentorshipSession.objects.filter(
        mentor=request.user,
        status='pending'
    ).select_related('student').order_by('scheduled_date', 'scheduled_time')[:10]
    
    # Get upcoming accepted sessions
    today = timezone.now().date()
    upcoming_sessions = MentorshipSession.objects.filter(
        mentor=request.user,
        status='accepted',
        scheduled_date__gte=today
    ).select_related('student').order_by('scheduled_date', 'scheduled_time')[:10]
    
    # Get old appointments
    old_appointments = Appointment.objects.filter(
        mentor=request.user
    ).select_related('user').order_by('-created_at')[:5]
    
    # Get availability slots
    # availability_slots = AvailabilitySlot.objects.filter(
    #     mentor=request.user,
    #     is_active=True
    # ).order_by('day_of_week', 'start_time')
    
    # Get content contributions
    # contributions = ContentContribution.objects.filter(
    #     author=request.user
    # ).order_by('-created_at')[:10]
    
    # Calculate stats
    total_pending = pending_sessions.count()
    completed_sessions_count = MentorshipSession.objects.filter(
        mentor=request.user,
        status='completed'
    ).count()
    
    context = {
        # 'mentor_profile': mentor_profile,
        'pending_sessions': pending_sessions,
        'upcoming_sessions': upcoming_sessions,
        'old_appointments': old_appointments,
        # 'availability_slots': availability_slots,
        # 'contributions': contributions,
        'total_pending': total_pending,
        'completed_sessions_count': completed_sessions_count,
    }
    
    return render(request, 'dashboard/mentor_dashboard.html', context)


@login_required
def mentor_content(request):
    if request.user.role !='mentor':
        messages.error(request,"⛔ Only mentors can add availability slots.")
        return redirect('home')
    if not request.user.is_approved:
        messages.error(request,"⏳ You must be approved by admin to access the mentor dashboard.")
        return redirect('home')
    contributions = ContentContribution.objects.filter(
        author=request.user
    ).order_by('-created_at')[:10]
    
    context={'contributions':contributions,}
    return render(request,'mentor/content.html',context)

# @login_required
# def mentor_profile(request):
#     if request.user.role !='mentor':
#         messages.error(request,"⛔ Only mentors can add availability slots.")
#         return redirect('home')
#     if not request.user.is_approved:
#         messages.error(request,"⏳ You must be approved by admin to access the mentor dashboard.")
#         return redirect('home')
#     mentor_profile, created = MentorProfile.objects.get_or_create(
#         user=request.user,
#         defaults={
#             'bio': getattr(request.user, 'bio', ''),
#             'expertise': getattr(request.user, 'expertise', ''),
#             'fee_30min': 10,
#             'fee_60min': 20,
#         }
#     )
    
#     # Handle profile update form submission
#     if request.method == 'POST':
#         bio = request.POST.get('bio', '').strip()
#         skills = request.POST.get('skills', '').strip()
#         fee_30m = request.POST.get('fee_30m', 10)
#         fee_60m = request.POST.get('fee_60m', 20)
        
#         if len(bio) > 500:
#             messages.error(request, "❌ Bio must be 500 characters or less.")
#             return redirect('mentor_dashboard')
        
#         try:
#             mentor_profile.bio = bio
#             mentor_profile.expertise = skills
#             mentor_profile.fee_30min = int(fee_30m) if fee_30m else 10
#             mentor_profile.fee_60min = int(fee_60m) if fee_60m else 20
#             mentor_profile.save()
            
#             if hasattr(request.user, 'bio'):
#                 request.user.bio = bio
#             if hasattr(request.user, 'expertise'):
#                 request.user.expertise = skills
#             request.user.save()
            
#             messages.success(request, "✅ Profile updated successfully!")
#             return redirect('mentor_dashboard')
            
#         except ValueError as e:
#             messages.error(request, "❌ Invalid fee values. Please enter valid numbers.")
#             return redirect('mentor_dashboard')
#         except Exception as e:
#             messages.error(request, f"❌ Error updating profile: {str(e)}")
#             return redirect('mentor_dashboard')
#      # Get availability slots
#     availability_slots = AvailabilitySlot.objects.filter(
#         mentor=request.user,
#         is_active=True
#     ).order_by('day_of_week', 'start_time')

#     context={
#         'mentor_profile': mentor_profile,
#         'availability_slots': availability_slots,
#     }
#     return render(request,'mentor/profile.html',context)

@login_required
def mentor_profile(request):
    if request.user.role != 'mentor':
        messages.error(request, "⛔ Only mentors can access this page.")
        return redirect('home')

    if not request.user.is_approved:
        messages.error(request, "⏳ You must be approved by admin.")
        return redirect('home')

    mentor_profile, created = MentorProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'bio': '',
            'expertise': '',
            'fee_30min': 10,
            'fee_60min': 20,
        }
    )

    if request.method == 'POST':
        mentor_profile.bio = request.POST.get('bio', '').strip()
        mentor_profile.expertise = request.POST.get('skills', '').strip()
        mentor_profile.fee_30min = request.POST.get('fee_30m') or 10
        mentor_profile.fee_60min = request.POST.get('fee_60m') or 20

        # Handle profile photo upload
        if request.FILES.get('profile_photo'):
            request.user.profile_photo = request.FILES['profile_photo']
            request.user.save()

        if len(mentor_profile.bio) > 500:
            messages.error(request, "❌ Bio must be under 500 characters.")
        else:
            mentor_profile.save()
            messages.success(request, "✅ Profile updated successfully!")

        return redirect(request.path)

    availability_slots = AvailabilitySlot.objects.filter(
        mentor=request.user,
        is_active=True
    ).order_by('day_of_week', 'start_time')

    return render(request, 'mentor/profile.html', {
        'mentor_profile': mentor_profile,
        'availability_slots': availability_slots,
    })



@login_required
def add_availability_slot(request):
    """Add new availability slot"""
    if request.user.role != 'mentor':
        messages.error(request, "⛔ Only mentors can add availability slots.")
        return redirect('home')
    
    if request.method == 'POST':
        day = request.POST.get('day')
        time_from = request.POST.get('time_from')
        time_to = request.POST.get('time_to')
        
        if day and time_from and time_to:
            existing = AvailabilitySlot.objects.filter(
                mentor=request.user,
                day_of_week=day,
                start_time=time_from,
                end_time=time_to,
                is_active=True
            ).exists()
            
            if existing:
                messages.warning(request, "⚠️ This availability slot already exists.")
            else:
                AvailabilitySlot.objects.create(
                    mentor=request.user,
                    day_of_week=day,
                    start_time=time_from,
                    end_time=time_to
                )
                messages.success(request, "✅ Availability slot added successfully!")
        else:
            messages.error(request, "❌ Please fill all fields.")
    
    return redirect('mentor_dashboard')


@login_required
def remove_availability_slot(request, slot_id):
    """Remove availability slot"""
    if request.user.role != 'mentor':
        messages.error(request, "⛔ Only mentors can remove availability slots.")
        return redirect('home')
    
    slot = get_object_or_404(AvailabilitySlot, id=slot_id, mentor=request.user)
    day = slot.get_day_of_week_display()
    time_range = f"{slot.start_time.strftime('%I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}"
    
    slot.delete()
    messages.success(request, f"✅ Removed availability: {day} {time_range}")
    return redirect('mentor_dashboard')


@login_required
def accept_session(request, session_id):
    """Accept a session request"""
    if request.user.role != 'mentor':
        messages.error(request, "⛔ Only mentors can accept sessions.")
        return redirect('home')
    
    session = get_object_or_404(MentorshipSession, id=session_id, mentor=request.user)
    
    if session.status != 'pending':
        messages.warning(request, "⚠️ This session has already been processed.")
        return redirect('mentor_dashboard')
    
    session.status = 'accepted'
    session.save()
    
    messages.success(request, f"✅ Session with {session.student.username} accepted!")
    return redirect('mentor_dashboard')


@login_required
def decline_session(request, session_id):
    """Decline a session request"""
    if request.user.role != 'mentor':
        messages.error(request, "⛔ Only mentors can decline sessions.")
        return redirect('home')
    
    session = get_object_or_404(MentorshipSession, id=session_id, mentor=request.user)
    
    if session.status != 'pending':
        messages.warning(request, "⚠️ This session has already been processed.")
        return redirect('mentor_dashboard')
    
    session.status = 'declined'
    session.save()
    
    messages.info(request, f"📋 Session with {session.student.username} declined.")
    return redirect('mentor_dashboard')


@login_required
def complete_session(request, session_id):
    """Mark session as completed"""
    if request.user.role != 'mentor':
        messages.error(request, "⛔ Only mentors can complete sessions.")
        return redirect('home')
    
    session = get_object_or_404(MentorshipSession, id=session_id, mentor=request.user)
    
    if session.status != 'accepted':
        messages.warning(request, "⚠️ Only accepted sessions can be marked as completed.")
        return redirect('mentor_dashboard')
    
    mentor_profile, created = MentorProfile.objects.get_or_create(
        user=request.user,
        defaults={'fee_30min': 10, 'fee_60min': 20}
    )
    
    session.status = 'completed'
    session.completed_at = timezone.now()
    session.save()
    
    mentor_profile.total_sessions += 1
    mentor_profile.total_earnings += session.fee_amount
    mentor_profile.save()
    
    messages.success(request, "✅ Session marked as completed!")
    return redirect('mentor_dashboard')


@login_required
def submit_content(request):
    if request.user.role != 'mentor':
        messages.error(request, "⛔ Only mentors can submit content.")
        return redirect('home')

    if request.method == 'POST':
        # --- NEW: Check existing content count ---
        existing_count = ContentContribution.objects.filter(author=request.user).count()
        if existing_count >= 5:
            messages.error(request, "❌ Limit reached! You can only have 5 contributions.")
            return redirect('mentor_content')
        # ------------------------------------------

        title = request.POST.get('title', '').strip()
        body = request.POST.get('body', '').strip()
        submit_type = request.POST.get('submit_type', 'draft')
        
        if not title:
            messages.error(request, "❌ Title is required.")
            return redirect('mentor_dashboard')
        
        if not body:
            messages.error(request, "❌ Content body is required.")
            return redirect('mentor_dashboard')
        
        # ✅ FIXED: Changed from 'pending' to 'published' for immediate publishing
        status = 'published' if submit_type == 'publish' else 'draft'
        
        # Create content
        content = ContentContribution(
            author=request.user,
            title=title,
            body=body,
            status=status
        )

        # ✅ Added: Save blog cover image if provided
        if request.FILES.get('images'):
            content.images = request.FILES['images']
        
        # ✅ FIXED: Set published_at when publishing
        if status == 'published':
            content.published_at = timezone.now()
        
        content.save()
        
    if status == 'published':
        messages.success(request, "✅ Content published successfully!")
    else:
        messages.success(request, "✅ Draft saved successfully!")
    return redirect('mentor_content')

@login_required
def edit_content(request, content_id):
    """View to load the edit form and handle the update logic."""
    
    # 1. Role Security Check
    if request.user.role != 'mentor':
        messages.error(request, "⛔ Only mentors can edit content.")
        return redirect('home')
    
    # 2. Ownership Security Check
    content = get_object_or_404(ContentContribution, id=content_id, author=request.user)
    
    # 3. Handle Form Submission (POST)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        body = request.POST.get('body', '').strip()
        submit_type = request.POST.get('submit_type', 'draft')
        
        if title and body:
            content.title = title
            content.body = body
            
            # Added: Save blog cover image on edit
            if request.FILES.get('content_image'):
                content.images = request.FILES['content_image']
            
            # Logic for publishing vs drafting
            if submit_type == 'publish':
                content.status = 'published'
                if not content.published_at:
                    content.published_at = timezone.now()
            else:
                content.status = 'draft'
            
            content.save()
            messages.success(request, "✅ Content updated successfully!")
            return redirect('mentor_dashboard')
        else:
            messages.error(request, "❌ Title and body are required.")
            # Fall through to render the form again with error
    
    # 4. Handle Initial Load (GET)
    # This renders a template where the user actually types the changes
    return render(request, 'mentor/edit_content_form.html', {
        'content': content
    })

@login_required
@require_POST
def delete_content(request, content_id):
    """Securely delete a content contribution"""
    # Ensure the user is a mentor
    if request.user.role != 'mentor':
        messages.error(request, "⛔ Unauthorized action.")
        return redirect('home')

    # Ensure the content exists AND belongs to the user
    content = get_object_or_404(ContentContribution, id=content_id, author=request.user)
    
    title = content.title # Store title for the message
    content.delete()
    
    messages.success(request, f"🗑️ '{title}' has been deleted.")
    return redirect('mentor_content')



# ==================== STUDENT/USER BOOKING VIEWS ====================

@login_required
def book_session(request, id):
    """Book a mentorship session with a mentor (NEW SYSTEM)"""
    mentor = get_object_or_404(CustomUser, id=id, role='mentor', is_approved=True)
    
    if request.user == mentor:
        messages.error(request, "⛔ You cannot book a session with yourself.")
        return redirect('mentor_detail', id=mentor.id)
    
    try:
        mentor_profile = MentorProfile.objects.get(user=mentor)
    except MentorProfile.DoesNotExist:
        mentor_profile = None

    if request.method == "POST":
        scheduled_date = request.POST.get('date')
        scheduled_time = request.POST.get('time')
        duration = int(request.POST.get('duration', 30))
        topic = request.POST.get('topic', '').strip()
        note = request.POST.get('note', '').strip()
        
        if not scheduled_date or not scheduled_time:
            messages.error(request, "❌ Please provide both date and time.")
            return redirect('book_session', id=mentor.id)
        
        if mentor_profile:
            token_fee = mentor_profile.fee_30min if duration == 30 else mentor_profile.fee_60min
        else:
            token_fee = 10 if duration == 30 else 20
        
        MentorshipSession.objects.create(
            student=request.user,
            mentor=mentor,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time,
            duration=duration,
            topic=topic,
            notes=note,
            fee_amount=token_fee,
            status='pending'
        )
        
        messages.success(request, f"✅ Session request sent to {mentor.username}! You'll be notified once they accept.")
        return redirect('user_sessions')
    
    availability_slots = AvailabilitySlot.objects.filter(
        mentor=mentor,
        is_active=True
    ).order_by('day_of_week', 'start_time')

    context = {
        'mentor': mentor,
        'mentor_profile': mentor_profile,
        'availability_slots': availability_slots,
        'today': timezone.now().date().isoformat(),
    }
    return render(request, 'book_appointments.html', context)


@login_required
def user_sessions(request):
    """View user's booked sessions"""
    my_sessions = MentorshipSession.objects.filter(
        student=request.user
    ).select_related('mentor').order_by('-created_at')
    
    today = timezone.now().date()
    pending_sessions = my_sessions.filter(status='pending')
    upcoming_sessions = my_sessions.filter(
        status='accepted',
        scheduled_date__gte=today
    ).order_by('scheduled_date', 'scheduled_time')
    past_sessions = my_sessions.filter(status='completed').order_by('-scheduled_date')
    declined_sessions = my_sessions.filter(status='declined')
    
    context = {
        'pending_sessions': pending_sessions,
        'upcoming_sessions': upcoming_sessions,
        'past_sessions': past_sessions,
        'declined_sessions': declined_sessions,
    }
    return render(request, 'user_sessions.html', context)


@login_required
def cancel_session(request, session_id):
    """Cancel a session booking"""
    session = get_object_or_404(MentorshipSession, id=session_id, student=request.user)
    
    if session.status == 'completed':
        messages.error(request, "⛔ Cannot cancel a completed session.")
        return redirect('user_sessions')
    
    session.status = 'cancelled'
    session.save()
    
    messages.info(request, f"📋 Session with {session.mentor.username} has been cancelled.")
    return redirect('user_sessions')


# ==================== BLOG/CONTENT VIEWS ====================

def blog_list(request):
    """Display all published mentor blog posts"""
    # ✅ FIXED: Order by created_at instead of published_at (fallback)
    blog_posts = ContentContribution.objects.filter(
        status='published'
    ).select_related('author').order_by('-created_at')
    
    context = {
        'blog_posts': blog_posts,
    }
    return render(request, 'mentor/blog_list.html', context)


def blog_detail(request, content_id):
    """Display a single blog post"""
    blog_post = get_object_or_404(
        ContentContribution, 
        id=content_id, 
        status='published'
    )
    
    # Increment view count
    blog_post.views_count += 1
    
    # ✅ FIXED: Set published_at if it's None (for old posts)
    if not blog_post.published_at:
        blog_post.published_at = timezone.now()
    
    blog_post.save()
    
    # Get author's mentor profile
    try:
        author_profile = MentorProfile.objects.get(user=blog_post.author)
    except MentorProfile.DoesNotExist:
        author_profile = None
    
    # Get related posts from same author
    # ✅ FIXED: Order by created_at instead of published_at
    related_posts = ContentContribution.objects.filter(
        author=blog_post.author,
        status='published'
    ).exclude(id=content_id).order_by('-created_at')[:3]
    
    context = {
        'blog_post': blog_post,
        'author_profile': author_profile,
        'related_posts': related_posts,
    }
    return render(request, 'mentor/blog_detail.html', context)
