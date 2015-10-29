from django import forms
from ChasingSomeoneApp.models.UserProfile import UserProfile, User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()
