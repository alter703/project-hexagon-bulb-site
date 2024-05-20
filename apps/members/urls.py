from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'members'

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/<uuid:uuid>', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile-edit'),

    path('profile/<uuid:uuid>/questions/', views.user_questions_view, name='user_questions'),
    path('profile/<uuid:uuid>/polls/', views.user_polls_view, name='user_polls'),
    path('profile/<uuid:uuid>/bookmarks/', views.user_polls_view, name='user_bookmarks'),
]