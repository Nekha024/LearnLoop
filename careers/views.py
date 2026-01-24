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


def career_predict(request):
    RADIO_OPTIONS = ["Strongly Disagree", "Not Sure", "Average", "Maybe", "Strongly Agree"]
    if request.method == "POST":
        form = CareerForm(request.POST)

        if form.is_valid():
            user_data = []
            
            # ✅ CRITICAL: Process features in the exact CSV order
            for csv_column in FEATURE_ORDER:
                # Find corresponding form field
                form_field = CSV_TO_FIELD.get(csv_column)
                
                if not form_field:
                    print(f"⚠️ Warning: No form field mapped to CSV column '{csv_column}'")
                    user_data.append(0)
                    continue
                
                # Get the value from cleaned form data
                value = form.cleaned_data.get(form_field)
                
                if value is None:
                    print(f"⚠️ Warning: No value for form field '{form_field}'")
                    user_data.append(0)
                    continue

                # ✅ Handle numeric inputs (int fields)
                if isinstance(value, int):
                    user_data.append(value)
                    print(f"✓ {csv_column}: {value} (numeric)")
                    continue

                # ✅ Handle Yes/No style fields
                if form_field in [
                    "self_learning_capability",
                    "Extra_courses_did",
                    "Taken_inputs_from_seniors",
                    "worked_in_teams",
                    "Introvert",
                ]:
                    mapped = YESNO_MAP.get(value, "no")
                    try:
                        encoded = encoders[csv_column].transform([mapped])[0]
                        user_data.append(encoded)
                        print(f"✓ {csv_column}: '{value}' → '{mapped}' → {encoded}")
                    except KeyError as e:
                        print(f"❌ Encoder missing: {csv_column} - {e}")
                        user_data.append(0)
                    except ValueError as e:
                        print(f"❌ Value error for {csv_column}: '{mapped}' - {e}")
                        user_data.append(0)
                    continue

                # ✅ Handle skill scale fields
                if form_field in [
                    "reading_and_writing_skills",
                    "memory_capability_score",
                ]:
                    mapped = SCALE_MAP.get(value, "medium")
                    try:
                        encoded = encoders[csv_column].transform([mapped])[0]
                        user_data.append(encoded)
                        print(f"✓ {csv_column}: '{value}' → '{mapped}' → {encoded}")
                    except KeyError as e:
                        print(f"❌ Encoder missing: {csv_column} - {e}")
                        user_data.append(0)
                    except ValueError as e:
                        print(f"❌ Value error for {csv_column}: '{mapped}' - {e}")
                        user_data.append(0)
                    continue

                # ✅ Handle normal categorical fields
                try:
                    encoded = encoders[csv_column].transform([str(value)])[0]
                    user_data.append(encoded)
                    print(f"✓ {csv_column}: '{value}' → {encoded}")
                except KeyError as e:
                    print(f"❌ Encoder missing: {csv_column} - {e}")
                    user_data.append(0)
                except ValueError as e:
                    print(f"❌ Unknown value for {csv_column}: '{value}' - {e}")
                    # Try to use first class as default
                    if csv_column in encoders:
                        user_data.append(0)
                    else:
                        user_data.append(0)

            print(f"\n✅ Final encoded input ({len(user_data)} features):")
            print(user_data)
            print(f"Expected features: {len(FEATURE_ORDER)}")

            # ✅ Validate feature count
            if len(user_data) != len(FEATURE_ORDER):
                return render(
                    request,
                    "careers/result.html",
                    {
                        "career": "Error: Feature mismatch",
                        "error": f"Expected {len(FEATURE_ORDER)} features, got {len(user_data)}"
                    },
                )

            # Make prediction
            try:
                prediction = model.predict([user_data])[0]
                predicted_job = encoders["Suggested Job Role"].inverse_transform([prediction])[0]

                print(f"✅ Prediction: {predicted_job}")

                return render(
                    request,
                    "careers/result.html",
                    {"career": predicted_job},
                )
            except Exception as e:
                print(f"❌ Prediction error: {e}")
                return render(
                    request,
                    "careers/result.html",
                    {"career": "Prediction failed", "error": str(e)},
                )

    else:
        form = CareerForm()

    return render(request, "careers/careerform.html", {"form": form})


def careers_view(request):
    return render(request, 'roadmap.html')




#api key and code snippet
from .services import get_code_rating
def code_evaluation_view(request):
    result = None
    if request.method == "POST":
        question = request.POST.get("question")
        code = request.POST.get("code_input")
        
        print(f"DEBUG: Received Question: {question}") # Step 1
        
        result = get_code_rating(question, code)
        
        print(f"DEBUG: Result from Gemini: {result}") # Step 2
        
    return render(request, "evaluate_code.html", {"result": result})