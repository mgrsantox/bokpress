from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from main import views
from main import models
from main import forms
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', TemplateView.as_view(template_name="base.html")),
    path('about/', TemplateView.as_view(template_name="about.html")),
    # path('contact/', views.ContactUsView.as_view(), name='contact'),
    path('contact/', views.contact, name='contact'),
    path('product/<slug:slug>/', DetailView.as_view(model=models.Product), name='product',),
    path('products/<slug:tag>/', views.ProductListView.as_view(), name='products'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        form_class=forms.AuthenticationForm,
    ),
        name='login'),


    # for address
    path(
        "address/",
        views.AddressListView.as_view(),
        name="address_list",
    ),
    path(
        "address/create/",
        views.AddressCreateView.as_view(),
        name="address_create",
    ),
    path(
        "address/<int:pk>/",
        views.AddressUpdateView.as_view(),
        name="address_update",
    ),
    path(
        "address/<int:pk>/delete/",
        views.AddressDeleteView.as_view(),
        name="address_delete",
    ),

]
