from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('question-hub/', include('apps.api.questionHub.urls')),
    path('poll-feed/', include('apps.api.pollFeed.urls')),
]