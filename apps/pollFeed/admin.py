from django.contrib import admin

from .models import Poll, Choice, Vote

# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_at')
    list_display_links = ('id', 'text')
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'votes')
    list_display_links = ('id', 'text',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'poll', 'choice',]
    list_filter = ['poll']
    search_fields = ['user__username', 'poll__text', 'choice__text']
    list_per_page = 20