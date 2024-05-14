from django.urls import path

from . import views

app_name = 'members'

urlpatterns = [
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    # path('signup/', views.signup_view, name='signup'),
    path('profile/<uuid:uuid>', views.ProfileDetailView.as_view(), name='profile_detail'),
    # path('profile/edit/', views.profile_edit_view, name='profile-edit'),
]