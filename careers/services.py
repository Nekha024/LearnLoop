import json
import time
from google import genai
from google.genai import errors
from django.conf import settings

def get_code_rating(question, dev_code):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    prompt = f"""
    Evaluate this code for the question: "{question}"
    Code to evaluate:
    {dev_code}
    
    Return a JSON object with:
    'score': (int 1-10),
    'skills_level': (Beginner/Intermediate/Advanced),
    'feedback': (Short review),
    'improvements': (list of strings)
    """

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
            
        except errors.ClientError as e:
            # FIX: Use .code instead of .status_code
            if e.code == 429: 
                if attempt < 2:  # Wait and retry if it's the 1st or 2nd attempt
                    time.sleep(10)
                    continue
                return {"error": "Rate limit exceeded. Please try again in a minute."}
            return {"error": f"Gemini API Error: {str(e)}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}
            
    return {"error": "Maximum retries reached."}