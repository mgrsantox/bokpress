from django import forms
from django.core.mail import send_mail
import logging

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
