from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Post, Comment

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a regular user
        self.user = User.objects.create_user(
            email="user@example.com",
            first_name="User",
            last_name="Test",
            password="userpass"
        )

        # Create an admin user
        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            password="adminpass"
        )

    def authenticate_user(self):
        response = self.client.post(reverse('login'), {
            "email": "user@example.com",
            "password": "userpass"
        })
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    def authenticate_admin(self):
        response = self.client.post(reverse('login'), {
            "email": "admin@example.com",
            "password": "adminpass"
        })
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "newpass"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            "email": "user@example.com",
            "password": "userpass"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_admin_can_create_post(self):
        self.authenticate_admin()
        response = self.client.post(reverse('post-list'), {
            "title": "Test Post",
            "body": "Admin-created post."
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_non_admin_cannot_create_post(self):
        self.authenticate_user()
        response = self.client.post(reverse('post-list'), {
            "title": "Unauthorized Post",
            "body": "Should not be allowed."
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_create_comment(self):
        self.authenticate_admin()
        post = Post.objects.create(title="Post", body="Post body")

        self.authenticate_user()
        response = self.client.post(reverse('comment-list-create'), {
            "post": post.id,
            "content": "This is a comment"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_unauthenticated_user_cannot_comment(self):
        post = Post.objects.create(title="Post", body="Post body")
        response = self.client.post(reverse('comment-list-create'), {
            "post": post.id,
            "content": "Unauthorized comment"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

