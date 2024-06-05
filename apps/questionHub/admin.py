from django.contrib import admin

from .models import Category, Question, Answer, Bookmark

# Register your models here.
@admin.register(Category)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'category')
    list_display_links = ('id', 'title')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'created_at', 'updated_at')
    list_display_links = ('id', 'content')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id','created_at')
