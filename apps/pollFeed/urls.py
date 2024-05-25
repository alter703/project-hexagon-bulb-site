from django.urls import path

from . import views

app_name = 'pollFeed'

urlpatterns = [
    path('', views.PollListView.as_view(), name='index'),
    path('poll/create/', views.create_poll, name='create'),
    path('poll/<uuid:id>', views.PollDetailView.as_view(), name='detail'),
    path('poll/<uuid:id>/vote/', views.VotePollView.as_view(), name='vote'),
    path('poll/<uuid:id>/close/', views.ClosePollView.as_view(), name='close'),
    path('poll/<uuid:id>/update/', views.PollUpdateView.as_view(), name='update'),
    path('poll/<uuid:id>/delete/', views.PollDeleteView.as_view(), name='delete'),

    path('search/', views.PollListView.as_view(), name='search'),
]
