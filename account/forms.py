from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    '''
    Form for input login data: username and password
    '''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    '''
    Form for entering a password during registration.
    '''
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        '''
        Checking the password for compliance with password2
        Returns the password value for registration user
        '''
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    '''
    Form for entering user data.
    '''
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    '''
    The form for entering the date of birth for the Profile model
    '''
    class Meta:
        model = Profile
        fields = ['date_of_birth']


class UserDetailForm(forms.ModelForm):
    '''
    The form for update user attributes by admin.
    '''
    class Meta:
        model = User
        fields = ['is_active', 'is_staff']
