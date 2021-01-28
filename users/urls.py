from django.urls import path

from .views import ProfileCreateView

urlpatterns = [
    path('signup', ProfileCreateView.as_view(), name='signup')
]
