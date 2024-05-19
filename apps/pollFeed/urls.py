from django.urls import path

from . import views

app_name = 'pollFeed'

urlpatterns = [
    path('', views.PollListView.as_view(), name='index'),
    path('poll/create/', views.create_poll, name='create'),
    path('poll/<int:id>', views.PollDetailView.as_view(), name='detail'),
    path('poll/<int:id>/vote/', views.vote_poll, name='vote'),
    path('poll/<int:id>/close/', views.close_poll, name='close'),
    path('poll/<int:id>/update/', views.PollUpdateView.as_view(), name='update'),
    path('poll/<int:id>/delete/', views.PollDeleteView.as_view(), name='delete'),

    path('search/', views.PollListView.as_view(), name='search'),
]
