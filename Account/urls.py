from django.urls import path
from django.contrib.auth import views as authviews

from Account.views import UserRegistrationView


urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', authviews.LoginView.as_view(), name='login'),
    path('logout/', authviews.LogoutView.as_view(), name='logout'),

    path('change-password/', authviews.PasswordChangeView.as_view(), name='change-password'),
    path('change-password/done/', authviews.PasswordChangeDoneView.as_view(), name='change-password-done'),
]