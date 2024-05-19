from django.contrib import admin
from .models import Poll, PollCategory, Answer, UserAnswer

# Register your models here.
class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ('content', 'is_correct')
    extra = 1


@admin.register(PollCategory)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(Answer)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'poll')
    list_display_links = ('id', 'content')


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'answer')
    list_display_links = ('id', 'poll')
