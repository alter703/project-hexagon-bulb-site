from django.urls import path

from . import views

app_name = 'pollFeed'

urlpatterns = [
    path('', views.PollListView.as_view(), name='index'),
    path('poll/create/', views.create_poll, name='create'),
    # path('poll/<int:id>', views.PollListView.as_view(), name='detail'),
]