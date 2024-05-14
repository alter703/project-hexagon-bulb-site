from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, CreateView
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


def signup_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile(user=user)
            profile.save()
            login(request, user)
            return redirect('main:index')
    return render(request, 'members/signup.html', {'form': form})

class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'members/login.html'

    def get_success_url(self):
        return reverse_lazy('main:index')

@login_required
def logout_view(request):
    logout(request)
    return redirect('main:index')
