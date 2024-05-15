from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.urls import reverse_lazy
from .forms import ProfileForm
from django.contrib import messages

from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, CreateView, UpdateView
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


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'members/signup.html'

    def form_valid(self, form):
        user = form.save()
        profile = Profile(user=user)
        profile.save()
        login(self.request, user)
        return redirect('main:index')


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'members/login.html'

    def get_success_url(self):
        return reverse_lazy('main:index')


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'members/profile_edit.html'
    # success_url = reverse_lazy('members:profile')  # Перенаправлення на профіль після успішного оновлення

    def get_success_url(self):
        return reverse_lazy('members:profile', kwargs={"uuid": self.request.user.profile.id})
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error updating profile')
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


@login_required
def logout_view(request):
    logout(request)
    return redirect('main:index')
