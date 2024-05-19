from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('whats-new/', views.whats_new_view, name='whats-new'),
]