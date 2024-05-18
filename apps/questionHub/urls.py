from django.urls import path

from . import views

app_name = 'questionHub'

urlpatterns = [
    path('', views.QuestionsListView.as_view(), name='index'),
    path('question/<slug:slug>', views.QuestionDetailView.as_view(), name='detail'),
    path('question/ask/', views.AskQuestionCreateView.as_view(), name='ask'),
    path('question/<slug:slug>/answer/', views.AnswerView.as_view(), name='answer-question'),
    path('question/<slug:slug>/delete/', views.QuestionDeleteView.as_view(), name='delete'),
    path('question/<slug:slug>/update/', views.QuestionUpdateView.as_view(), name='update'),
    path('question/<slug:slug>/close/', views.close_question, name='close'),
]