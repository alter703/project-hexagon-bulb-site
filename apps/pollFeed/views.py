from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Poll, Choice, Vote
from .forms import CreatePollForm, ChoiceForm

# Create your views here.
class PollListView(ListView):
    model = Poll
    template_name = "pollFeed/index.html"
    context_object_name = 'polls'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('author').order_by('?')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['open_polls'] = Poll.objects.filter(is_closed=False)
        context['recent_polls'] = Poll.objects.filter(is_closed=True)[:5]  # Відобразити тільки 5 найновіших опитувань
        return context


class PollDetailView(DetailView):
    model = Poll
    template_name = 'pollFeed/detail.html'
    context_object_name = 'poll'

    def get_queryset(self):
        return Poll.objects.select_related('author', 'author__profile')

    def get_object(self, queryset=None):
        return get_object_or_404(self.get_queryset(), id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_has_voted = Vote.objects.filter(user=self.request.user, poll=self.object).exists()
        context['user_has_voted'] = user_has_voted
        if user_has_voted:
            user_vote = Vote.objects.get(user=self.request.user, poll=self.object)
            context['user_vote'] = user_vote.choice
        return context


@login_required
def create_poll(request):
    if request.method == "POST":
        poll_form = CreatePollForm(request.POST)
        choice_forms = [ChoiceForm(request.POST, request.FILES, prefix=str(i)) for i in range(0, 5)]

        if poll_form.is_valid() and all(answer_form.is_valid() for answer_form in choice_forms):
            poll = poll_form.save(commit=False)
            poll.author = request.user
            poll.save()

            valid_answers = [answer_form for answer_form in choice_forms if answer_form.cleaned_data.get('text')]

            if len(valid_answers) < 2:
                messages.error(request, "You must type at least two choices!")
                return redirect('pollFeed:create')

            for answer_form in choice_forms:
                if answer_form.cleaned_data.get('text'):
                    answer = answer_form.save(commit=False)
                    answer.poll = poll
                    answer.author = request.user
                    answer.save()

            return redirect('pollFeed:index')
    else:
        poll_form = CreatePollForm()
        answer_forms = [ChoiceForm(prefix=str(i)) for i in range(0, 5)]
    return render(request, "pollFeed/create_poll.html", {"answer_forms": answer_forms, "poll_form": poll_form})


def vote_poll(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    if request.method == 'POST':
        try:
            selected_choice = poll.choices.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            messages.error(request, "You didn't select a choice.")
            return redirect('pollFeed:detail', pk=poll.pk)
        else:
            selected_choice.votes += 1
            selected_choice.save()
            messages.success(request, "Your vote has been recorded.")
            return redirect('pollFeed:detail', id=poll.id)
    else:
        return render(request, "pollFeed/detail.html")
    

def close_poll(request, id):
    poll = get_object_or_404(Poll, id=id)

    if request.method == 'POST':
        if poll.author == request.user:
            poll.is_closed = True
            poll.save()
            messages.success(request, "Poll has been closed. Check the results!")
        # else:
        #     messages.error(request, "You are not autho to close this poll.")
        return redirect('pollFeed:detail', id=id)
    return redirect('pollFeed:detail', id=id)