from django.forms import ModelForm, CharField, PasswordInput, EmailInput, TextInput, Textarea
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        widgets = {
            'message': Textarea(attrs={'cols': 50, 'rows': 1}),
        }


class AuthUserForm(AuthenticationForm, ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RegisterUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

        widgets = {
            'password': PasswordInput(attrs={
                'id': 'password-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"] = CharField(
            max_length=40,
            min_length=5)
        self.fields["first_name"] = CharField(
            max_length=40
        )
        self.fields["last_name"] = CharField(
            max_length=40
        )

        validator_user = RegexValidator(r'^[a-z0-9]*$')
        validator_password = RegexValidator(r'^[a-zA-Z0-9-=$!|?*+./]*$')
        validator_name = RegexValidator(r'^[a-zA-Z-]*$')
        self.fields['username'].validators = [validator_user]
        self.fields['password'].validators = [validator_password]
        self.fields['first_name'].validators = [validator_name]
        self.fields['last_name'].validators = [validator_name]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
