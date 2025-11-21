from django.urls import path
from sem4.views import LoginView, ProfileView, login_view, profile_view

app_name = "sem4"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
