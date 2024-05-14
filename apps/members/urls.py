from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'members'

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/<uuid:uuid>', views.ProfileDetailView.as_view(), name='profile-detail'),
    # path('profile/edit/', views.profile_edit_view, name='profile-edit'),
]