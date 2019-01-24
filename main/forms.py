from django import forms
from django.core.mail import send_mail
import logging
from django.contrib.auth.forms import(
    UserCreationForm as DjangoUserCreationForm)
from django.contrib.auth.forms import UsernameField
from . import models

from django.contrib.auth import authenticate

logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=200)
    message = forms.CharField(max_length=600, widget=forms.Textarea)

    def send_mail(self):
        logger.info("send email to customer")
        message = "From: {0}\n{1}".format(self.cleaned_data['name'], self.cleaned_data['message'],)

        send_mail(
            "site message",
            message,
            "site@bokpress.domain",
            ["customerservice@bokpress.domain"],
            fail_silently=False,
        )

# User creation form


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = models.User
        fields = ("email",)
        field_classes = {"email": UsernameField}

    def send_mail(self):
        logger.info(
            "Sending Signup email for email =%s",
            self.cleaned_data["email"],
        )

        message = "Welcome {}".format(self.cleaned_data["email"])
        send_mail(
            "Welcome to bokpress",
            message,
            "site@bokpress.domain",
            [self.cleaned_data["email"]],
            fail_silently=True,
        )
# for login Login


class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        strip=False, widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):

        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user = authenticate(
                self.request, email=email, password=password)
            if self.user is None:
                raise forms.ValidationError(
                    "invalid email/password combination.")
            logger.info(
                "Authenicate successfully for email=%s", email
            )
        return self.cleaned_data

    def get_user(self):
        return self.user
