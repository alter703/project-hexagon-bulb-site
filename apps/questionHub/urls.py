from django.urls import path

from . import views

app_name = 'questionHub'

urlpatterns = [
    path('', views.QuestionsListView.as_view(), name='index'),
    path('question/<slug:slug>', views.QuestionDetailView.as_view(), name='detail'),
    path('question/ask/', views.AskQuestionCreateView.as_view(), name='ask'),
]