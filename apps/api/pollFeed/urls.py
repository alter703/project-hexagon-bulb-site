from django.urls import path

from . import views

# app_name = 'pollFeed'

urlpatterns = [
    path('', views.PollListAPIView.as_view(), name='index'),
    path('poll/<uuid:id>/', views.PollDetailAPIView.as_view(), name='detail'),
]