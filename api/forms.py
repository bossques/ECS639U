from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import DateField, ImageField, DateInput, ClearableFileInput, EmailField, EmailInput, ModelForm

from .models import User


class RegisterForm(UserCreationForm):
    date_of_birth = DateField(
        label="Date Of Birth",
        widget=DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    profile_image = ImageField(
        label="Profile Picture",
        widget=ClearableFileInput(attrs={'class': 'form-control-file'}),
        required=False
    )
    email = EmailField(
        label="Email Address",
        widget=EmailInput(attrs={'class': 'form-control', 'type': 'email'}),
        required=True
    )

    class Meta:
        fields = UserCreationForm.Meta.fields + ('date_of_birth', 'profile_image', 'email')
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class ModifyForm(ModelForm):
    date_of_birth = DateField(required=True)
    profile_image = ImageField(required=False)
    email = EmailField(required=True)

    class Meta:
        fields = ['date_of_birth', 'profile_image', 'email']
        model = User
