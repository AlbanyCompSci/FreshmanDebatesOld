from django import forms
from django.contrib.auth.models import User


class InfoEditForm(forms.ModelForm):
    is_staff = forms.BooleanField(label="Is Teacher", required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_staff')


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30, error_messages={'required': '\"First name\" cannot be left blank'})
    last_name = forms.CharField(max_length=30, error_messages={'required': '\"Last name\" cannot be left blank'})
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, error_messages={'required': 'Password cannot be left bank'})
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, error_messages={'required': 'Please retype your password'})
    is_staff = forms.BooleanField(label="Is Teacher", required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get("email")).count() > 0:
            raise forms.ValidationError("Already an account under this email")
        return self.cleaned_data.get("email")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
