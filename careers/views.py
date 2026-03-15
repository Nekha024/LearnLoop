from django.shortcuts import render
import joblib
import numpy as np
from .forms import CareerForm

# Load model & encoders once
model = joblib.load("careers/ml/career_model.pkl")
encoders = joblib.load("careers/ml/encoders.pkl")

# UI range → dataset mappings
YESNO_MAP = {
    "Not at all": "no",
    "Maybe": "no",
    "Average": "yes",
    "Sometimes": "yes",
    "Of course": "yes",
}

SCALE_MAP = {
    "Not at all": "poor",
    "Maybe": "poor",
    "Average": "medium",
    "Sometimes": "medium",
    "Of course": "excellent",
}

# ✅ CRITICAL: Define the EXACT order of features as in your training CSV
FEATURE_ORDER = [
    'Logical quotient rating',
    'hackathons',
    'coding skills rating',
    'public speaking points',
    'self-learning capability?',
    'Extra-courses did',
    'certifications',
    'workshops',
    'reading and writing skills',
    'memory capability score',
    'Interested subjects',
    'interested career area',  # ✅ Remove trailing space if you retrained
    'Type of company want to settle in?',
    'Taken inputs from seniors or elders',
    'Interested Type of Books',
    'Management or Technical',
    'hard/smart worker',
    'worked in teams ever?',
    'Introvert',
]

# Django field → dataset column mapping
FIELD_TO_CSV = {
    # Numeric fields
    'Logical_quotient_rating': 'Logical quotient rating',
    'hackathons': 'hackathons',
    'coding_skills_rating': 'coding skills rating',
    'public_speaking_points': 'public speaking points',
    
    # Categorical fields
    'certifications': 'certifications',
    'workshops': 'workshops',
    'Interested_subjects': 'Interested subjects',
    'interested_career_area': 'interested career area',
    'Type_company_settle': 'Type of company want to settle in?',
    'Interested_type_of_books': 'Interested Type of Books',
    'Management_or_Technical': 'Management or Technical',
    'hard_smart_worker': 'hard/smart worker',
    
    # Yes/No fields
    'self_learning_capability': 'self-learning capability?',
    'Extra_courses_did': 'Extra-courses did',
    'Taken_inputs_from_seniors': 'Taken inputs from seniors or elders',
    'worked_in_teams': 'worked in teams ever?',
    'Introvert': 'Introvert',
    
    # Scale fields
    'reading_and_writing_skills': 'reading and writing skills',
    'memory_capability_score': 'memory capability score',
}

# Create reverse mapping: CSV column → form field
CSV_TO_FIELD = {v: k for k, v in FIELD_TO_CSV.items()}


def careers_view(request):
    return render(request, 'roadmap.html')




#api key and code snippet

import json
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from groq import Groq  # Import the correct library
from .models import CodingQuestion, UserCodingProfile
import os
from groq import Groq

# Initialize the Groq client with your key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@login_required
def code_arena(request):
    questions = CodingQuestion.objects.all()
    question = random.choice(questions) if questions.exists() else None
    
    stats, _ = UserCodingProfile.objects.get_or_create(user=request.user)
    return render(request, 'careers/arena.html', {
        'question': question, 
        'stats': stats
    })

@login_required
def evaluate_code(request):
    if request.method == "POST":
        try:
            user_code = request.POST.get('code')
            q_id = request.POST.get('question_id')
            question = CodingQuestion.objects.get(id=q_id)

            # Groq implementation using llama-3.3-70b-versatile
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a code judge. Return ONLY a JSON object with these keys: 'score' (int 0-100), 'feedback' (string), 'rating' ('Good', 'Average', 'Low')."
                    },
                    {
                        "role": "user", 
                        "content": f"Problem: {question.description}\nUser Code: {user_code}"
                    }
                ],
                response_format={"type": "json_object"} # Forces valid JSON output
            )

            # No more complex cleaning needed; Groq JSON mode handles it
            result = json.loads(completion.choices[0].message.content)

            # Update User Statistics
            profile, _ = UserCodingProfile.objects.get_or_create(user=request.user)
            profile.total_score += result.get('score', 0)
            profile.attempts += 1
            profile.save()

            return JsonResponse({
                'score': result.get('score'),
                'feedback': result.get('feedback'),
                'rating': profile.skill_rating,
                'attempts': profile.attempts
            })
        except Exception as e:
            print(f"Evaluation Error: {e}")
            return JsonResponse({'error': f'AI Evaluation failed: {str(e)}'}, status=500)
            
    return JsonResponse({'error': 'Unauthorized'}, status=403)



#CareerQuiz

import json
import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from .questions import QUESTIONS, CATEGORIES, TOTAL_QUESTIONS
from .groq_service import get_career_prediction, ROADMAPS
from .models import CareerAssessment

logger = logging.getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def assessment_view(request):
    """Render the full assessment page with all 30 questions."""
    context = {
        "questions": QUESTIONS,
        "categories": CATEGORIES,
        "total_questions": TOTAL_QUESTIONS,
    }
    return render(request, "career_predictor/assessment.html", context)


@require_http_methods(["POST"])
def predict_view(request):
    """Handle prediction form submission and return JSON result."""
    try:
        body = json.loads(request.body)
        answers = body.get("answers", {})

        # Basic validation
        if len(answers) < TOTAL_QUESTIONS:
            return JsonResponse({
                "error": f"Please answer all {TOTAL_QUESTIONS} questions. You answered {len(answers)}."
            }, status=400)

        # Get prediction from Groq
        prediction = get_career_prediction(answers)

        if "error" in prediction:
            return JsonResponse({"error": prediction["error"]}, status=500)

        # Save to database
        try:
            top_careers = prediction.get("top_careers", [])
            assessment = CareerAssessment.objects.create(
                session_key=request.session.session_key or "",
                answers=answers,
                top_career_1=top_careers[0]["role"] if len(top_careers) > 0 else "",
                top_career_2=top_careers[1]["role"] if len(top_careers) > 1 else "",
                top_career_3=top_careers[2]["role"] if len(top_careers) > 2 else "",
                score_1=top_careers[0].get("score", 0) if len(top_careers) > 0 else 0,
                score_2=top_careers[1].get("score", 0) if len(top_careers) > 1 else 0,
                score_3=top_careers[2].get("score", 0) if len(top_careers) > 2 else 0,
                raw_prediction=prediction.get("raw", ""),
                ip_address=get_client_ip(request),
                user=request.user if request.user.is_authenticated else None,
            )
            prediction["assessment_id"] = assessment.id
        except Exception as e:
            logger.error(f"DB save error: {e}")
            # Continue even if saving fails

        return JsonResponse(prediction)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request format."}, status=400)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return JsonResponse({"error": "Something went wrong. Please try again."}, status=500)


def roadmap_view(request, role_slug):
    """AJAX endpoint to get roadmap for a specific role."""
    # Convert slug back to role name
    role_name = role_slug.replace("-", " ").title()

    # Try exact match
    if role_name in ROADMAPS:
        return JsonResponse({
            "role": role_name,
            "description": ROADMAPS[role_name]["description"],
            "roadmap": ROADMAPS[role_name]["roadmap"],
        })

    # Try fuzzy match
    for key in ROADMAPS:
        if key.lower() == role_name.lower():
            return JsonResponse({
                "role": key,
                "description": ROADMAPS[key]["description"],
                "roadmap": ROADMAPS[key]["roadmap"],
            })

    return JsonResponse({"error": "Role not found"}, status=404)
