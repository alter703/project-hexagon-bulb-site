from django.urls import path

from . import views

app_name = 'pollFeed'

urlpatterns = [
    path('', views.PollsListView.as_view(), name='index'),
    # path('poll/<int:pk>', views.QuestionDetailView.as_view(), name='detail'),
    path('poll/publish/', views.create_poll_view, name='publish'),
]