from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from main import forms
from main import models
from django.http import HttpResponseRedirect


# for usercreation
import logging
from django.contrib.auth import login, authenticate
from django.contrib import messages

# Create your views here.

# Product View


class ProductListView(ListView):
    template_name = "main/templates/product_list.html"
    paginate_by = 4

    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None
        if tag != "all":
            self.tag = get_object_or_404(
                models.ProductTag, slug=tag
            )
        if self.tag:
            products = models.Product.objects.active().filter(
                tags=self.tag)
        else:
            products = models.Product.objects.active()
        return products.order_by("name")


class ContactUsView(FormView):
    template_name = "contact.html"
    form_class = forms.ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            form.send_mail()
            return HttpResponseRedirect('/')
    else:
        form = forms.ContactForm()
    return render(request, 'contact.html', {'form': form})



# For user creation
logger = logging.getLogger(__name__)


class SignupView(FormView):
    template_name = "signup.html"
    form_class = forms.UserCreationForm

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        logger.info(
            "New Sign up for email=%s through SignupView", email
        )

        user = authenticate(email=email, password=raw_password)
        login(self.request, user)

        form.send_mail()

        messages.info(
            self.request, "You signup Successfully"
        )
        return response
