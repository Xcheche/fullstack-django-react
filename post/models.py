from django.db import models

from CoreRoot.abstract import AbstractModel, AbstractManager


class PostManager(AbstractManager):
    pass


class Post(AbstractModel):
    author = models.ForeignKey(
        to="user.User", related_name="posts", on_delete=models.CASCADE
    )
    body = models.TextField()
    edited = models.BooleanField(default=False)
    objects = PostManager()

    def __str__(self):
        return f"Post by {self.author.username} at {self.created}"

    class Meta:
        db_table = "'core.post'"
