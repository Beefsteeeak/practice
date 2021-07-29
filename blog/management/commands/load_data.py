from blog.models import Comment, Post

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from faker import Faker

from lorem_text import lorem

fake = Faker()


class Command(BaseCommand):
    """
    This command is for inserting User, Comment, Post into database.
    """

    def handle(self, *args, **options):
        User.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()

        # create 10 users
        users = [User(username=fake.unique.user_name(),
                      email=fake.email(),
                      password=make_password(fake.password(length=10, special_chars=False)))
                 for _ in range(10)]
        User.objects.bulk_create(users)

        # create 2 posts for every user
        posts = []
        for user in User.objects.all():
            for _ in range(2):
                posts.append(Post(headline=fake.unique.catch_phrase(),
                                  short_description=lorem.sentence(),
                                  description=lorem.paragraph(),
                                  image=fake.image_url(),
                                  blank=False,
                                  user=user))
        Post.objects.bulk_create(posts)

        # create 10 comments for every post
        comments = []
        for post in Post.objects.all():
            for _ in range(10):
                comments.append(Comment(text=lorem.paragraph(),
                                        is_published=True,
                                        post=post))
        Comment.objects.bulk_create(comments)
