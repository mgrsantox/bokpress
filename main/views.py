from django.shortcuts import render
from django.views.generic.edit import FormView
from main import forms
from django.http import HttpResponseRedirect
# Create your views here.


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
