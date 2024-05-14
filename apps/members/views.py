from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.views.generic import DetailView
from django.contrib.auth import logout

from .models import Profile


# Create your views here.
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'members/profile_detail.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'uuid'  # Змінюємо pk_url_kwarg на 'uuid'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user')
        return queryset


@login_required
def logout_view(request):
    logout(request)
    return redirect('main:index')
