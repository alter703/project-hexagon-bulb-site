from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/<uuid:id>/', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile-edit'),

    path('profile/<uuid:id>/questions/', views.user_questions_view, name='user_questions'),
    path('profile/<uuid:id>/polls/', views.user_polls_view, name='user_polls'),
    path('profile/<uuid:id>/bookmarks/', views.user_bookmarks_view, name='user_bookmarks'),
]
