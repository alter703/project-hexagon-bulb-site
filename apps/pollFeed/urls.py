from django.urls import path

from . import views

app_name = 'pollFeed'

urlpatterns = [
    path('', views.index, name='index'),
    # path('poll/<int:pk>', views.QuestionDetailView.as_view(), name='detail'),
    # path('poll/publish/', views.AskQuestionCreateView.as_view(), name='ask'),
]