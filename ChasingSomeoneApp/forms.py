from django import forms
from ChasingSomeoneApp.models.UserProfile import UserProfile, User
from django.contrib.auth.forms import UserCreationForm

# class UserForm(forms.ModelForm):
class SignUpForm (UserCreationForm):

    email = forms.EmailField(label='Email Address', max_length=75)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("This email address exists. Did you forget your password?")
        except User.DoesNotExist:
            return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_active = False
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()
