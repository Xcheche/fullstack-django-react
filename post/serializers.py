from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from CoreRoot.abstract.serializers import AbstractSerializer
from post.models import Post
from user.models import User

# Serializer for the Post model.
class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="public_id"
    )
    # This checks if the author of the post is the same as the user making the request.
    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can't create a post for another user.")

        return value

    class Meta:
        model = Post
        fields = ["id", "author", "body", "edited", "created", "updated"]
        read_only_fields = ["edited"]