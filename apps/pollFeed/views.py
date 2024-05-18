from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
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
        queryset = (
            queryset.select_related('author', 'author__profile')  # Використання select_related для вибору пов'язаних об'єктів через JOIN
            .prefetch_related('choices')  # Використання prefetch_related для вибору пов'язаних об'єктів через окремі запити
        )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['open_polls'] = Poll.objects.filter(is_closed=False).select_related('author', 'author__profile').prefetch_related('choices')
        context['recent_polls'] = Poll.objects.all().select_related('author').prefetch_related('choices')[:3]
        return context


class PollDetailView(LoginRequiredMixin, DetailView):
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

def vote_poll(request, id):
    poll = get_object_or_404(Poll, id=id)

    if request.method == 'POST':
        try:
            selected_choice = poll.choices.get(id=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            messages.error(request, "You didn't select a valid choice.")
            return redirect('pollFeed:detail', id=poll.id)
        else:
            # Отримання користувача, який голосує
            user = request.user

            # Створення та збереження об'єкта Vote в базі даних
            vote = Vote(user=user, poll=poll, choice=selected_choice)
            vote.save()

            # Збільшення лічильника голосів для обраного варіанту відповіді
            selected_choice.votes += 1
            selected_choice.save()

            messages.success(request, "Your vote has been recorded.")
            return redirect('pollFeed:detail', id=poll.id)
    else:
        return render(request, "pollFeed/detail.html")

class PollDeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        question = get_object_or_404(Poll, id=id, author=request.user)
        question.delete()
        messages.success(request, 'Poll was deleted successfully')
        return redirect('pollFeed:index')


class PollUpdateView(LoginRequiredMixin, UpdateView):
    model = Poll
    form_class = CreatePollForm
    template_name = 'questionHub/edit_question.html'
    context_object_name = 'question'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'Poll was updated successfully')
        return reverse_lazy('pollFeed:detail', kwargs={'id': self.object.id})

    def form_invalid(self, form):
        messages.error(self.request, 'Error while updating Poll')
        return super().form_invalid(form)


def close_poll(request, id):
    poll = get_object_or_404(Poll, id=id)

    if request.method == 'POST':
        if poll.author == request.user:
            poll.is_closed = True
            poll.save()
            messages.success(request, "Poll has been closed. Check the results!")

        return redirect('pollFeed:detail', id=id)
    return redirect('pollFeed:detail', id=id)
