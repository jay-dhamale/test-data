from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        # read_only_fields = ('password',)

    # def to_representation(self, instance):
    #     return super().to_representation(instance)
