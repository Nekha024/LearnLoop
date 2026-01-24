from django import forms

RANGE_CHOICES = [
    ("Not at all", "Not at all"),
    ("Maybe", "Maybe"),
    ("Average", "Average"),
    ("Sometimes", "Sometimes"),
    ("Of course", "Of course"),
]

CERTIFICATIONS = [
    ("information security", "Information Security"),
    ("shell programming", "Shell Programming"),
    ("machine learning", "Machine Learning"),
    ("fullstack", "Full Stack Development"),
]

WORKSHOP_TYPES = [
    ("testing", "Testing"),
    ("cloud computing", "Cloud Computing"),
    ("web development", "Web Development"),
    ("data analytics", "Data Analytics"),
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

COMPANY_TYPES = [
    ("BPA", "BPA"),
    ("Cloud Services", "Cloud Services"),
    ("product development", "Product Development"),
    ("service based", "Service Based"),
]

MANAGEMENT_OR_TECH = [
    ("Management", "Management"),
    ("Technical", "Technical"),
]

HARD_SMART = [
    ("hard worker", "Hard Worker"),
    ("smart worker", "Smart Worker"),
]


class CareerForm(forms.Form):
    Logical_quotient_rating = forms.IntegerField(min_value=0, max_value=10)
    hackathons = forms.IntegerField(min_value=0, max_value=50)
    coding_skills_rating = forms.IntegerField(min_value=0, max_value=10)
    public_speaking_points = forms.IntegerField(min_value=0, max_value=10)

    self_learning_capability = forms.ChoiceField(choices=RANGE_CHOICES)
    Extra_courses_did = forms.ChoiceField(choices=RANGE_CHOICES)
    Taken_inputs_from_seniors = forms.ChoiceField(choices=RANGE_CHOICES)
    worked_in_teams = forms.ChoiceField(choices=RANGE_CHOICES)
    Introvert = forms.ChoiceField(choices=RANGE_CHOICES)

    reading_and_writing_skills = forms.ChoiceField(choices=RANGE_CHOICES)
    memory_capability_score = forms.ChoiceField(choices=RANGE_CHOICES)

    certifications = forms.ChoiceField(choices=CERTIFICATIONS)
    workshops = forms.ChoiceField(choices=WORKSHOP_TYPES)

    Interested_subjects = forms.ChoiceField(choices=SUBJECTS)
    interested_career_area = forms.ChoiceField(choices=CAREER_AREAS)

    Type_company_settle = forms.ChoiceField(choices=COMPANY_TYPES)
    Interested_type_of_books = forms.ChoiceField(choices=SUBJECTS)

    Management_or_Technical = forms.ChoiceField(choices=MANAGEMENT_OR_TECH)
    hard_smart_worker = forms.ChoiceField(choices=HARD_SMART)
