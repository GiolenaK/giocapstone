from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'profile_photo']

    def save(self, commit=True):
            user = super().save(commit=False)
            if not user.user_type:
                user.user_type = "Simple"  # because when signing up, error popped up
                
            if not user.fosterer_status:
                user.fosterer_status = "None"  # default, staff changes these

            if commit:
                user.save()
            return user
    
    def clean_fosterer_status(self):
            user_type = self.cleaned_data.get("user_type")
            fosterer_status = self.cleaned_data.get("fosterer_status")

            if user_type in ["admin", "staff"] and fosterer_status != "none":
                return "none" 

            return fosterer_status