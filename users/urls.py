from django.urls import path

from .views import UserCreateView, UserRetrieveView

urlpatterns = [
    path('signup', UserCreateView.as_view(), name='signup'),
    path('me', UserRetrieveView.as_view(), name='me'),
]
