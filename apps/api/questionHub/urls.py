from django.urls import path

from . import views

# app_name = 'questionHub'

urlpatterns = [
    path('question/<uuid:id>', views.question_detail, name='detail'),
    path('question/ask/', views.question_post, name='ask')
]
