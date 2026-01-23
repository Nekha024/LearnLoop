from django.shortcuts import render

# Create your views here.
def careers_view(request):
    return render(request, 'roadmap.html')


import joblib
import numpy as np
from django.shortcuts import render
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

# Django field → dataset column mapping
FIELD_MAP = {
    # Categorical fields
    "Interested_subjects": "Interested subjects",
    "interested_career_area": "interested career area",
    "Type_company_settle": "Type of company want to settle in?",
    "Interested_type_of_books": "Interested Type of Books",
    "Management_or_Technical": "Management or Technical",
    "hard_smart_worker": "hard/smart worker",

    # Yes / No style fields
    "self_learning_capability": "self-learning capability?", # Matches your CSV exactly
    "Extra_courses_did": "Extra-courses did",                 # Matches your CSV exactly
    "Taken_inputs_from_seniors": "Taken inputs from seniors or elders",
    "worked_in_teams": "worked in teams ever?",
    "Introvert": "Introvert",

    # Scale fields
    "reading_and_writing_skills": "reading and writing skills",
    "memory_capability_score": "memory capability score",
}


def career_predict(request):
    if request.method == "POST":
        form = CareerForm(request.POST)

        if form.is_valid():
            user_data = []

            # Loop through form fields and encode
            for field, value in form.cleaned_data.items():
                encoder_key = FIELD_MAP.get(field, field)

                # Numeric inputs
                if isinstance(value, int):
                    user_data.append(value)
                    continue

                # Yes / No style ranges
                if field in [
                    "self_learning_capability",
                    "Extra_courses_did",
                    "Taken_inputs_from_seniors",
                    "worked_in_teams",
                    "Introvert",
                ]:
                    mapped = YESNO_MAP.get(value, "no")
                    encoded = encoders[encoder_key].transform([mapped])[0]
                    user_data.append(encoded)
                    continue

                # Skill scale ranges
                if field in [
                    "reading_and_writing_skills",
                    "memory_capability_score",
                ]:
                    mapped = SCALE_MAP.get(value, "medium")
                    encoded = encoders[encoder_key].transform([mapped])[0]
                    user_data.append(encoded)
                    continue

                # Normal categorical fields
                encoded = encoders[encoder_key].transform([value])[0]
                user_data.append(encoded)

            print("Final encoded input:", user_data)

            prediction = model.predict([user_data])[0]

            predicted_job = encoders[
                "Suggested Job Role"
            ].inverse_transform([prediction])[0]

            return render(
                request,
                "careers/result.html",
                {"career": predicted_job},
            )

    else:
        form = CareerForm()

    return render(request, "careers/careerform.html", {"form": form})
