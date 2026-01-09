from django import forms

from django import forms

YES_NO = [("yes", "Yes"), ("no", "No")]

BOOK_TYPES = [
    ("Series", "Series"),
    ("Autobiographies", "Autobiographies"),
    ("Travel", "Travel"),
    ("Self-help", "Self-help"),
    ("Educational", "Educational"),
]

COMPANY_TYPES = [
    ("BPA", "BPA"),
    ("Cloud Services", "Cloud Services"),
    ("product development", "Product Development"),
    ("service based", "Service Based"),
]

WORKSHOP_TYPES = [
    ("testing", "Testing"),
    ("cloud computing", "Cloud Computing"),
    ("web development", "Web Development"),
    ("data analytics", "Data Analytics"),
]

CERTIFICATIONS = [
    ("information security", "Information Security"),
    ("shell programming", "Shell Programming"),
    ("machine learning", "Machine Learning"),
    ("fullstack", "Full Stack Development"),
]

SUBJECTS = [
    ("programming", "Programming"),
    ("Management", "Management"),
    ("data engineering", "Data Engineering"),
    ("networks", "Networks"),
]

CAREER_AREAS = [
    ("testing", "Testing"),
    ("system developer", "System Developer"),
    ("Business process analyst", "Business Process Analyst"),
    ("data science", "Data Science"),
]

MANAGEMENT_OR_TECH = [
    ("Management", "Management"),
    ("Technical", "Technical"),
]

HARD_SMART = [
    ("hard worker", "Hard Worker"),
    ("smart worker", "Smart Worker"),
]

READING_SKILLS = [
    ("poor", "Poor"),
    ("medium", "Medium"),
    ("excellent", "Excellent"),
]

MEMORY_SCORE = [
    ("poor", "Poor"),
    ("medium", "Medium"),
    ("excellent", "Excellent"),
]


class CareerForm(forms.Form):
    Logical_quotient_rating = forms.IntegerField(min_value=0, max_value=10)
    hackathons = forms.IntegerField(min_value=0, max_value=50)
    coding_skills_rating = forms.IntegerField(min_value=0, max_value=10)
    public_speaking_points = forms.IntegerField(min_value=0, max_value=10)
    

    self_learning_capability = forms.ChoiceField(choices=YES_NO)
    Extra_courses_did = forms.ChoiceField(choices=YES_NO)

    certifications = forms.ChoiceField(choices=CERTIFICATIONS)
    workshops = forms.ChoiceField(choices=WORKSHOP_TYPES)

    reading_and_writing_skills = forms.ChoiceField(choices=READING_SKILLS)
    memory_capability_score = forms.ChoiceField(choices=MEMORY_SCORE)

    Interested_subjects = forms.ChoiceField(choices=SUBJECTS)
    interested_career_area = forms.ChoiceField(choices=CAREER_AREAS)

    Type_company_settle = forms.ChoiceField(choices=COMPANY_TYPES)
    Taken_inputs_from_seniors = forms.ChoiceField(choices=YES_NO)

    Interested_type_of_books = forms.ChoiceField(choices=BOOK_TYPES)

    Management_or_Technical = forms.ChoiceField(choices=MANAGEMENT_OR_TECH)
    hard_smart_worker = forms.ChoiceField(choices=HARD_SMART)

    worked_in_teams = forms.ChoiceField(choices=YES_NO)
    Introvert = forms.ChoiceField(choices=YES_NO)
