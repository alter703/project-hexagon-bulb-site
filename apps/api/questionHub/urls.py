from django.urls import path

from . import views

# app_name = 'questionHub'

urlpatterns = [
    path('', views.QuestionAPIView.as_view(), name='index'),
    path('question/<uuid:id>/', views.question_detail, name='detail'),
    path('question/random/', views.question_random, name='random-detail'),
    path('question/ask/', views.QuestionAskAPIView.as_view(), name='ask'),

    path('category/all/', views.CategoryAPIView.as_view(), name='categories'),
]
