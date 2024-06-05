from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View, TemplateView, FormView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.main.mixins import ProfanityCheckMixin

from .models import Poll, Choice, Vote
from .forms import CreatePollForm
from .mixins import PollMultipleObjectMixin, PollSingleObjectMixin

# Create your views here.
class PollListView(PollMultipleObjectMixin, ListView):
    template_name = "pollFeed/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_polls'] = Poll.objects.select_related('author').prefetch_related('choices')[:3]
        return context


class PollDetailView(PollSingleObjectMixin, DetailView):
    template_name = 'pollFeed/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_has_voted = False
        user_vote = None

        if self.request.user.is_authenticated:
            vote = Vote.objects.filter(user=self.request.user, poll=self.object).first()
            if vote:
                user_has_voted = True
                user_vote = vote.choice

        context['user_has_voted'] = user_has_voted
        context['user_vote'] = user_vote
        return context


class CreatePollView(LoginRequiredMixin, ProfanityCheckMixin, View):
    form_class = CreatePollForm
    template_name = "pollFeed/create_poll.html"

    def get(self, request, *args, **kwargs):
        poll_form = self.form_class()
        return render(request, self.template_name, {"poll_form": poll_form})

    def post(self, request, *args, **kwargs):
        poll_form = self.form_class(request.POST)

        if poll_form.is_valid():
            fields = [field for field in poll_form.fields.keys()]

            poll = poll_form.save(commit=False)
            poll.author = request.user
            poll.save()

            # Saving choices
            choice_texts = [poll_form.cleaned_data.get(f'choice{i}') for i in range(1, 5)]
            valid_choices = [text for text in choice_texts if text]

            if len(valid_choices) < 2:
                messages.error(request, "You must type at least two choices!")
                poll.delete()
                return redirect('pollFeed:create')
            elif not self.check_profanity(poll_form, fields):
                poll.delete()
                return redirect('pollFeed:create')
                         
            for text in valid_choices:
                Choice.objects.create(poll=poll, text=text, author=request.user)

            messages.success(request, 'Your Poll is created successfully!')
            return redirect('pollFeed:index')
        
        return render(request, self.template_name, {"poll_form": poll_form})    


class VotePollView(View):
    def post(self, request, id):
        poll = get_object_or_404(Poll, id=id)
        selected_choice_id = request.POST.get('choice')
        
        # Check if a choice was selected
        if not selected_choice_id:
            messages.error(request, "Please select a choice.")
            return redirect('pollFeed:detail', id=poll.id)

        selected_choice = get_object_or_404(Choice, id=selected_choice_id)

        # Check if the user is authenticated
        if request.user.is_authenticated:
            user = request.user
            # Check if the user has already voted
            if Vote.objects.filter(user=user, poll=poll).exists():
                messages.error(request, "You have already voted in this poll.")
                return redirect('pollFeed:detail', id=poll.id)
            is_anonymous = False
        else:
            # Check if the user has already voted anonymously
            session_key = f'voted_{poll.id}'
            if request.session.get(session_key, False):
                messages.error(request, "You have already voted in this poll.")
                return redirect('pollFeed:detail', id=poll.id)
            user = None
            is_anonymous = True

        # Create the vote
        vote = Vote(user=user, poll=poll, choice=selected_choice, is_anonymous=is_anonymous)
        vote.save()
        selected_choice.votes += 1
        selected_choice.save()

        if is_anonymous:
            request.session[session_key] = True

        messages.success(request, "Your vote has been recorded.")
        return redirect('pollFeed:detail', id=poll.id)

    def get(self, request, id):
        return render(request, "pollFeed/detail.html")


class PollDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        poll = get_object_or_404(Poll, id=id, author=request.user)
        poll.delete()
        messages.success(request, 'Poll was deleted successfully')
        return redirect('pollFeed:index')


class PollUpdateView(LoginRequiredMixin, UpdateView):
    model = Poll
    form_class = CreatePollForm
    template_name = 'pollFeed/edit_poll.html'
    context_object_name = 'poll'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'Poll was updated successfully')
        return reverse_lazy('pollFeed:detail', kwargs={'id': self.object.id})

    def form_invalid(self, form):
        messages.error(self.request, 'Error while updating Poll')
        return super().form_invalid(form)


class ClosePollView(LoginRequiredMixin, View):
    def post(self, request, id):
        poll = get_object_or_404(Poll, id=id)
        if poll.author == request.user:
            poll.is_closed = True
            poll.save()
            messages.success(request, "Poll has been closed. Check the results!")
        else:
            messages.error(request, "You do not have permission to close this poll.")
        return redirect('pollFeed:detail', id=id)

    def get(self, request, *args, **kwargs):
        return redirect('pollFeed:detail', id=kwargs['id'])
