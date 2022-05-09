from django.urls import path
from .views import (
    UserLoginView, Blocked
)

urlpatterns = [
    path("login/", UserLoginView.as_view()),
    path("blocked/", Blocked.as_view())
]
