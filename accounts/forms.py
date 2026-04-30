from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class DynamicPlaceholderMixin:
    def apply_placeholders(self):
        for field_name in self.fields:
            self.fields[field_name].help_text = None
            label = self.fields[field_name].label or field_name.replace('_', ' ').title()
            self.fields[field_name].widget.attrs.update({'placeholder': label})
            
            # Field choices
            if hasattr(self.fields[field_name], 'choices'):
                choices = list(self.fields[field_name].choices)
                if choices and (choices[0][0] in ('', 'unknown') or choices[0][1] in ('---------', 'Unknown')):
                    choices[0] = ('', f"Select {label}")
                elif not choices or (choices[0][0] != '' and choices[0][0] != 'unknown'):
                    choices.insert(0, ('', f"Select {label}"))
                self.fields[field_name].choices = choices

            # Widget choices (needed for some widget types)
            if hasattr(self.fields[field_name].widget, 'choices'):
                w_choices = list(self.fields[field_name].widget.choices)
                if w_choices and (w_choices[0][0] in ('', 'unknown') or w_choices[0][1] in ('---------', 'Unknown')):
                    w_choices[0] = ('', f"Select {label}")
                elif not w_choices or (w_choices[0][0] != '' and w_choices[0][0] != 'unknown'):
                    w_choices.insert(0, ('', f"Select {label}"))
                self.fields[field_name].widget.choices = w_choices
                
            if isinstance(self.fields[field_name].widget, (forms.FileInput, forms.ClearableFileInput)):
                self.fields[field_name].widget.attrs.update({'class': 'file-input'})

class CustomUserCreationForm(UserCreationForm, DynamicPlaceholderMixin):
    class Meta:
        model = CustomUser
        fields = ('username', 'email','phone_number', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_placeholders()

class CustomAuthenticationForm(AuthenticationForm, DynamicPlaceholderMixin):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_placeholders()

class MentorCreationForm(UserCreationForm, DynamicPlaceholderMixin):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'previous_experience','gender','profile_photo','profession','experience_years','expertise','bio','linkedin','portfolio','intro_video', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_placeholders()
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'mentor'
        if commit:
            user.save()
        return user

class MentorLoginForm(AuthenticationForm, DynamicPlaceholderMixin):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_placeholders()


from django import forms
from .models import CustomUser

class MentorProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'expertise', 'available_from', 'available_to']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'maxlength': 500,
                'class': 'mt-1 block w-full rounded-lg border border-gray-300 shadow-sm p-3',
                'placeholder': 'Tell students about your experience and what you can help with...'
            }),
            'expertise': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border border-gray-300 shadow-sm p-3',
                'placeholder': 'Python, Django, PostgreSQL, React'
            }),
            'available_from': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full rounded-lg border border-gray-300 shadow-sm p-3'
            }),
            'available_to': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full rounded-lg border border-gray-300 shadow-sm p-3'
            }),
        }
        labels = {
            'bio': 'Professional Bio (Max 500 characters)',
            'expertise': 'Key Skills (Comma Separated)',
            'available_from': 'Available From',
            'available_to': 'Available To',
        }

class CustomUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = "__all__"
        widgets = {
            "gender": forms.Select(
                choices=CustomUser.GENDER_CHOICES
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 THIS LINE KILLS THE '---------' OPTION
        self.fields["gender"].choices = CustomUser.GENDER_CHOICES
        self.fields["gender"].required = True