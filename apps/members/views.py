from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .forms import ProfileForm
from django.contrib import messages

from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth import logout

from .models import Profile

from apps.questionHub.models import *
from apps.pollFeed.models import *

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self посилається на конкретний об'єкт конкретної моделі (в Profile - user, biography, image...)
        context['user_questions'] = Question.objects.filter(author=self.object.user).select_related('author', 'category').prefetch_related('answers')
        context['user_polls'] = Poll.objects.filter(author=self.object.user).select_related('author').prefetch_related('choices')
        context['bookmarks'] = Bookmark.objects.filter(user=self.object.user).select_related('user', 'question').prefetch_related('question__author')
        return context

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'members/signup.html'

    
    def form_valid(self, form):
        user = form.save()
        profile = Profile(user=user)
        profile.save()
        login(self.request, user)
        messages.success(self.request, "Welcome to our family!")
        return redirect('main:index')

    def form_invalid(self, form):
        return super().form_invalid(form)


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'members/login.html'

    def get_success_url(self):
        return reverse_lazy('main:index')

    def form_valid(self, form):
        messages.success(self.request, f"You've signed in!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'members/profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('members:profile', kwargs={"uuid": self.request.user.profile.id})
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile is updated')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        return Profile.objects.select_related('user').get(user=self.request.user)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You've signed out")
    return redirect('main:index')


def user_questions_view(request, uuid):
    profile = get_object_or_404(Profile, id=uuid)
    questions = Question.objects.filter(author=profile.user).select_related('author', 'category').prefetch_related('answers')
    paginator = Paginator(questions, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'members/user_questions.html', {'profile': profile, 'page_obj': page_obj})

def user_polls_view(request, uuid):
    profile = get_object_or_404(Profile, id=uuid)
    polls = Poll.objects.filter(author=profile.user).select_related('author').prefetch_related('choices')
    paginator = Paginator(polls, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'members/user_polls.html', {'profile': profile, 'page_obj': page_obj})

def user_bookmarks_view(request, uuid):
    profile = get_object_or_404(Profile, id=uuid)
    bookmarks = Bookmark.objects.filter(author=profile.user).select_related('author').prefetch_related('choices')
    paginator = Paginator(bookmarks, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'members/user_polls.html', {'profile': profile, 'page_obj': page_obj})
