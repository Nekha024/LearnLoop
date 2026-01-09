from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email','phone_number', 'password1', 'password2')
    
    #Method to remove the Help Texts from passwords and username
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Call the parent's init first
        
        # Turn off the username help text
        if 'username' in self.fields:
            self.fields['username'].help_text = None
            self.fields['username'].label = None
        
        # Turn off the password bullet points (on 'password1')
        if 'password1' in self.fields:
            self.fields['password1'].help_text = None
            
        # (Optional) Turn off the password confirmation help text
        if 'password2' in self.fields:
            self.fields['password2'].help_text = None
        
        if 'phone_number' in self.fields:
            self.fields['phone_number'].help_text = None
            
        # Adding placeholders to the form fields
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Username'}
        )
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Email address'}
        )
        self.fields['phone_number'].widget.attrs.update(
            {'placeholder': 'Phone number'}
        )
        self.fields['password1'].widget.attrs.update(
            {'placeholder': 'Password'}
        )
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Repeat Password'}
        )

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Username'}
        )
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Password'}
        )
        

class MentorCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'previous_experience','gender','profile_photo','profession','experience_years','expertise','bio','linkedin','portfolio','intro_video', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Call the parent's init first
        
        # Turn off the username help text
        # if 'username' in self.fields:
        #     self.fields['username'].help_text = None
        
        # # Turn off the password bullet points (on 'password1')
        # if 'password1' in self.fields:
        #     self.fields['password1'].help_text = None
            
        # # (Optional) Turn off the password confirmation help text
        # if 'password2' in self.fields:
        #     self.fields['password2'].help_text = None
        
        # if 'phone_number' in self.fields:
        #     self.fields['phone_number'].help_text = None
        
        # Put the names of all fields you want to clear in a list
        fields_to_clear = ['username', 'password1', 'password2', 'phone_number']
        # Loop through the list and set help_text to None if the field exists
        for field_name in fields_to_clear:
            if field_name in self.fields:
                self.fields[field_name].help_text = None
        
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Username'}
        )
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Email address'}
        )
        self.fields['phone_number'].widget.attrs.update(
            {'placeholder': 'Phone number'}
        )
        self.fields['previous_experience'].widget.attrs.update(
            {'placeholder': 'Previous Experience'}
        )
        self.fields['password1'].widget.attrs.update(
            {'placeholder': 'Password'}
        )
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Repeat Password'}
        )
        self.fields['profession'].widget.attrs.update(
            {'placeholder': 'Profession'}
        )
        self.fields['experience_years'].widget.attrs.update(
            {'placeholder': 'Years of Experience'}
        )
        self.fields['expertise'].widget.attrs.update(
            {'placeholder': 'Area of Expertise'}
        )
        self.fields['bio'].widget.attrs.update(
            {'placeholder': 'Brief Bio'}
        )
        self.fields['linkedin'].widget.attrs.update(
            {'placeholder': 'LinkedIn Profile URL'}
        )
        self.fields['portfolio'].widget.attrs.update(
            {'placeholder': 'Portfolio URL'}
        )
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'mentor'
        if commit:
            user.save()
        return user

class MentorLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)


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
