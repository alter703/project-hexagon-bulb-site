from django.urls import path

from . import views

# app_name = 'questionHub'

urlpatterns = [
    path('', views.QuestionAPIView.as_view(), name='index'),
    path('question/<uuid:id>/', views.QuestionDetailAPIView.as_view(), name='detail'),
    path('question/random/', views.QuestionRandomAPIView.as_view(), name='random-detail'),
    path('question/ask/', views.QuestionManageAPIView.as_view(), name='ask'),
    path('question/<uuid:id>/update/', views.QuestionManageAPIView.as_view(), name='update'),
    path('question/<uuid:id>/delete/', views.QuestionManageAPIView.as_view(), name='delete'),

    path('category/all/', views.CategoryListAPIView.as_view(), name='categories'),
]
