# blog/tests.py
from django.test import TestCase
from django.conf import settings
from members.models import MemberProfile

User = settings.AUTH_USER_MODEL

from .models import Post

class BlogTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user
        testuser1 = MemberProfile.objects.create_user(email='test@gmail.com', first_name='first_name', last_name='last_name', password='dshjdFHF1252')
        testuser1.save()

        # Create a blog post
        test_post = Post.objects.create(
            author=testuser1, title='Blog title', body='Body content...')
        test_post.save()

    def test_blog_content(self):
        post = Post.objects.get(id=1)
        expected_author = f'{post.author}'
        expected_title = f'{post.title}'
        expected_body = f'{post.body}'
        self.assertEqual(expected_author, 'test@gmail.com')
        self.assertEqual(expected_title, 'Blog title')
        self.assertEqual(expected_body, 'Body content...')


