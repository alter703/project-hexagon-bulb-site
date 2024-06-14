from django.urls import path
from . import views

app_name = 'questionHub'

urlpatterns = [
    path('', views.QuestionsListView.as_view(), name='index'),
    path('question/ask/', views.AskQuestionView.as_view(), name='ask'),
    path('question/<uuid:id>/', views.QuestionDetailView.as_view(), name='detail'),
    path('question/<uuid:id>/answer/', views.AnswerView.as_view(), name='answer-question'),
    path('question/<uuid:id>/delete/', views.QuestionDeleteView.as_view(), name='delete'),
    path('question/<uuid:id>/update/', views.QuestionUpdateView.as_view(), name='update'),
    path('question/<uuid:id>/close/', views.CloseQuestionView.as_view(), name='close'),
    path('question/<uuid:id>/bookmark/', views.BookmarkView.as_view(), name='bookmark'),
    
    path('search/', views.QuestionsListView.as_view(), name='search'),
    path('category/<int:id>/', views.QuestionsByCategoryListView.as_view(), name='select-category'),
]