from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username="igor", password="password123")

    def test_can_list_posts(self):
        igor = User.objects.get(username="igor")
        Post.objects.create(owner=igor, title="a title")
        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username="igor", password="password123")
        count = Post.objects.count()
        self.assertEqual(count, 0)
        response = self.client.post("/posts/", {"title": "a title"})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_create_post(self):
        count = Post.objects.count()
        self.assertEqual(count, 0)
        response = self.client.post("/posts/", {"title": "a title"})
        count = Post.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        igor = User.objects.create_user(username="igor", password="password123")
        bart = User.objects.create_user(username="bart", password="password456")
        Post.objects.create(
            owner=igor, title="a title", content="igor's content"
        )
        Post.objects.create(
            owner=bart, title="another title", content="bart's content"
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get("/posts/1/")
        self.assertEqual(response.data["title"], "a title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_retrieve_post_using_invalid_id(self):
        response = self.client.get("/posts/777/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_update_post_if_owner(self):
        self.client.login(username="igor", password="password123")
        response = self.client.put("/posts/1/", {"title": "my updated title"})
        self.assertEqual(response.data["title"], "my updated title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_update_post_if_not_owner(self):
        self.client.login(username="igor", password="password123")
        response = self.client.put("/posts/2/", {"title": "my updated title"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
