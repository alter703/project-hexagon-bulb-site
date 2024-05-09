from django.urls import path

from . import views

app_name = 'questionHub'

urlpatterns = [
    path('', views.QuestionsListView.as_view(), name='index'),
    path('question/<int:pk>', views.QuestionDetailView.as_view(), name='detail')
]