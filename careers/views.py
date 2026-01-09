from django.shortcuts import render

# Create your views here.
def careers_view(request):
    return render(request, 'roadmap.html')


import joblib
import numpy as np
from django.shortcuts import render
from .forms import CareerForm

# Load ML model and encoders once
model = joblib.load("careers/ml/career_model.pkl")
encoders = joblib.load("careers/ml/encoders.pkl")


def career_predict(request):
    if request.method == "POST":
        form = CareerForm(request.POST)
        if form.is_valid():
            user_data = []

            # Loop through form fields and encode
            for field, value in form.cleaned_data.items():
                if field in encoders:
                    value = encoders[field].transform([value])[0]
                else:
                    # Handle yes/no or boolean-like
                    if isinstance(value, str):
                        v = value.strip().lower()

                        if v in ["yes", "true", "1", "on"]:
                            value = 1
                        elif v in ["no", "false", "0", "off"]:
                            value = 0
                        else:
                            # Try to match encoder by *value type* (catch 'poor', 'good', etc.)
                            for enc_name, enc in encoders.items():
                                try:
                                    # If this encoder can handle it, use it
                                    value = enc.transform([value])[0]
                                    break
                                except Exception:
                                    continue
                            else:
                                # Last resort: try numeric conversion
                                try:
                                    value = float(value)
                                except ValueError:
                                    print(f"⚠️ Could not encode field '{field}' with value '{value}'")
                    else:
                        # Numeric already, just append
                        pass

                user_data.append(value)

            # Debugging: see what’s going into the model
            print("Encoded input data:", user_data)
            print("Data types:", [type(v) for v in user_data])

            # Make sure everything is numeric
            try:
                prediction = model.predict([user_data])[0]
            except Exception as e:
                print("Model prediction failed:", e)
                return render(
                    request,
                    "careers/result.html",
                    {"career": "Error: invalid input — check encoding."},
                )

            # Decode the prediction back to human-readable job title
            predicted_job = encoders["Suggested Job Role"].inverse_transform([prediction])[0]

            return render(request, "careers/result.html", {"career": predicted_job})

    else:
        form = CareerForm()

    return render(request, "careers/careerform.html", {"form": form})
