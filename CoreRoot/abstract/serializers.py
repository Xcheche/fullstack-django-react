from rest_framework import serializers
class AbstractSerializer(serializers.ModelSerializer):
    """Base serializer for all models in the project.

    This serializer is used as a base for all serializers in the project. It
    provides a common interface for all serializers and can be extended with
    common functionality in the future if needed.

    Note that this serializer does not include any fields or validation logic.
    It is simply a base class for all serializers to inherit from.
    """
    id = serializers.UUIDField(source='public_id',read_only=True, format='hex')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)