from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import DateField, ImageField, DateInput, ClearableFileInput, EmailField, EmailInput

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

    class Meta:
        fields = UserCreationForm.Meta.fields + ('date_of_birth', 'profile_image')
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
