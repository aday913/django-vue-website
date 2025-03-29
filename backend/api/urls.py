from django.urls import path
from .views import RegisterView, LoginView, PostList, CommentListCreate

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('posts/', PostList.as_view(), name='post-list'),
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
]

