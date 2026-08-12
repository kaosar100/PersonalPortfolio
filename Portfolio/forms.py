from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import ContactMessage, Education, Experience, Profile, Project, Skill


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values(): field.widget.attrs.setdefault('class', 'input')


class RegistrationForm(StyledModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    class Meta:
        model = User
        fields = ('username', 'email')
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists(): raise forms.ValidationError('An account already uses this email address.')
        return email
    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'): self.add_error('confirm_password', 'Passwords do not match.')
        if cleaned.get('password'): validate_password(cleaned['password'], self.instance)
        return cleaned
    def save(self, commit=True):
        user = super().save(commit=False); user.set_password(self.cleaned_data['password'])
        if commit: user.save()
        return user


class LoginForm(forms.Form):
    identifier = forms.CharField(label='Username or email')
    password = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values(): field.widget.attrs['class'] = 'input'


class ProfileForm(StyledModelForm):
    class Meta:
        model = Profile; exclude = ('user',)
        widgets = {'bio': forms.Textarea(attrs={'rows': 4})}

class SkillForm(StyledModelForm):
    class Meta:
        model = Skill; fields = ('name', 'proficiency')
        widgets = {'proficiency': forms.NumberInput(attrs={'min': 0, 'max': 100})}

class EducationForm(StyledModelForm):
    class Meta:
        model = Education; exclude = ('user', 'created_at')
        widgets = {'start_date': forms.DateInput(attrs={'type': 'date'}), 'end_date': forms.DateInput(attrs={'type': 'date'}), 'description': forms.Textarea(attrs={'rows': 4})}

class ExperienceForm(StyledModelForm):
    class Meta:
        model = Experience; exclude = ('user', 'created_at')
        widgets = {'start_date': forms.DateInput(attrs={'type': 'date'}), 'end_date': forms.DateInput(attrs={'type': 'date'}), 'description': forms.Textarea(attrs={'rows': 4})}

class ProjectForm(StyledModelForm):
    class Meta:
        model = Project; exclude = ('user', 'created_at')
        widgets = {'summary': forms.Textarea(attrs={'rows': 5}), 'completed_on': forms.DateInput(attrs={'type': 'date'})}

class ContactForm(StyledModelForm):
    class Meta:
        model = ContactMessage; fields = ('name', 'email', 'subject', 'message')
        widgets = {'message': forms.Textarea(attrs={'rows': 6})}
