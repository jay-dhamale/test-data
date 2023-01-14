from rest_framework import serializers
from .models import User
from collections import OrderedDict


class AtomicSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        action = self.context['view'].action
        # print(self.context)
        permission = self.context['request'].user == instance.id 
        # print(self.Meta.fields)
        # # print(bulk-update)
        # print(action)
        # print(permission)

        if action == 'list':
            return OrderedDict({key:data[key] for key in data if key in self.Meta.list_fields})
        if action == 'retrieve':
            if not permission:
                return data
            return OrderedDict({key:data[key] for key in data if key in self.Meta.get_fields})
        return data


class UserSerializer(AtomicSerializer):
    time = serializers.SerializerMethodField()

    def get_time(self, instance):
        return "I am time ago"
    class Meta:
        model = User
        fields = "__all__"
        list_fields = ["id", "first_name",]
        get_fields = ["first_name", "last_name", "email", "id"]
        # other_fields = 

        # read_only_fields = ('password',)

   