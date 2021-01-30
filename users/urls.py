from django.urls import path

from .views import UserCreateView, UserLoginView, UserRetrieveView

urlpatterns = [
    path('signup', UserCreateView.as_view(), name='signup'),
    path('signin', UserLoginView.as_view(), name='signin'),
    path('me', UserRetrieveView.as_view(), name='me'),
]
