from django.urls import path
from django.views.generic import TemplateView
from main import views


urlpatterns = [
    path('', TemplateView.as_view(template_name="base.html")),
    path('about/', TemplateView.as_view(template_name="about.html")),
    # path('contact/', views.ContactUsView.as_view(), name='contact'),
    path('contact/', views.contact, name='contact'),
]
