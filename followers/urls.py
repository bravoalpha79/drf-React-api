from django.urls import path
from follower import views

urlpatterns = [
    path("followers/", views.FollowerList.as_view()),
    path("followers/<int:pk>/", views.FollowerDetail.as_view()),
]