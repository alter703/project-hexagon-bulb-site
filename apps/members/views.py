from django.shortcuts import render

from django.views.generic import DetailView
from .models import Profile


# Create your views here.
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'members/profile_detail.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'uuid'  # Змінюємо pk_url_kwarg на 'uuid'
