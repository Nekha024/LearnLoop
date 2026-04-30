from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from mentor.models import MentorshipSession
from .models import ChatMessage
from django.utils import timezone

@login_required
def chat_room(request, session_id):
    session = get_object_or_404(MentorshipSession, id=session_id)
    
    # Security: Only mentor or student of the session can access
    if request.user != session.mentor and request.user != session.student:
        return redirect('home')
    
    # Requirement: Only after acceptance or completion
    if session.status not in ['accepted', 'completed']:
        return redirect('home')
    
    messages = session.messages.all().order_by('timestamp')
    
    # Mark messages as read if the current user is the receiver
    session.messages.filter(receiver=request.user, is_read=False).update(is_read=True)
    
    receiver = session.student if request.user == session.mentor else session.mentor
    
    base_template = 'dashboard/mentorbase.html' if request.user.role == 'mentor' else 'dashboard/userbase.html'
    
    context = {
        'chat_session': session,
        'chat_messages': messages,
        'other_user': receiver,
        'base_template': base_template
    }
    return render(request, 'chat/chat_room.html', context)

@login_required
def send_message(request, session_id):
    if request.method == 'POST':
        session = get_object_or_404(MentorshipSession, id=session_id)
        
        if request.user != session.mentor and request.user != session.student:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        message_text = request.POST.get('message', '').strip()
        if message_text:
            receiver = session.student if request.user == session.mentor else session.mentor
            ChatMessage.objects.create(
                session=session,
                sender=request.user,
                receiver=receiver,
                message=message_text
            )
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
            
        return redirect('chat_room', session_id=session_id)
            
    return redirect('home')
