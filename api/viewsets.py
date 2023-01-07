
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
# from .models import Users
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend



# Atomic View
class AtomicViewSet(ModelViewSet):
    # renderer_classes = AtomicJsonRenderer

    # # TODO  write queryset
    # def get_queryset(self):
    #     """
    #     1. filter inactive user
    #     2. filter level zero user
    #     3. Comments
    #     """
    #     if self.request.user_level == 0:
    #         return self.serializer_class.Meta.model.objects.all()
    #     if self.request.user_level == 5:
    #         return self.serializer_class.Meta.model.objects.exclude(userId__user_level=0)
    #     return self.serializer_class.Meta.model.objects.exclude(userId__is_active=False).exclude(userId__user_level=0)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    def validate_data(self, data):
        serializer_class = self.serializer_class or self.get_serializer_class()
        new_data = []
        # if serializer_class.Meta.model == Users:
        #     for item in data:
        #         if "email" not in item:
        #             raise serializers.ValidationError(f'This Email field not provided for: {item}')
        #         email_check = {"email": item["email"]}
        #         if serializer_class.Meta.model.objects.filter(**email_check).exists():
        #             raise serializers.ValidationError(f'This data already exists: {item}')
        #         else:
        #             new_data.append(serializer_class.Meta.model(**item))
        #     return serializer_class.Meta.model.objects.bulk_create(new_data)
        for item in data:
            if serializer_class.Meta.model.objects.filter(**item).exists():
                raise serializers.ValidationError(f'This data already exists: {item}')
            else:
                new_data.append(serializer_class.Meta.model(**item))
        return serializer_class.Meta.model.objects.bulk_create(new_data)

    def validate_ids(self, data, field="id", unique=True):
        # new_data = []
        serializer_class = self.serializer_class or self.get_serializer_class()
        for item in data:
            if "id" not in item:
                raise serializers.ValidationError(f'Id Not provided {item}')

            if not serializer_class.Meta.model.objects.filter(id=item['id']).exists():
                raise serializers.ValidationError(f'Id does not Exists {item}')
            else:
                serializer_class.Meta.model.objects.filter(id=item['id']).update(**item)
        return [x[field] for x in data]

    @action(detail=False, methods=['post'], url_path='bulk-update')
    def bulk_update(self, request, *args, **kwargs):
        try:
            serializer_class = self.serializer_class or self.get_serializer_class()
            if not request.user.is_superuser:
                return Response("Unauthorized user", status=status.HTTP_403_FORBIDDEN)
            if not isinstance(request.data, list):
                raise ValidationError('Request body must be a list')
            if request.data == []:
                raise ValidationError('Empty data not permitted')
            ids = self.validate_ids(request.data)
            instances = serializer_class.Meta.model.objects.filter(id__in=ids)
            fields = [f.name for f in serializer_class.Meta.model._meta.get_fields()]
            _ = serializer_class.Meta.model.objects.bulk_update(instances, fields)
            serializer = serializer_class(instances, many=True, partial=True, context={"context": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request, *args, **kwargs):
        serializer_class = self.serializer_class or self.get_serializer_class()
        if not request.user.is_superuser:
            return Response("Unauthorized user", status=status.HTTP_403_FORBIDDEN)
        if not isinstance(request.data, list):
            raise ValidationError('Request body must be a list')
        if request.data == []:
            raise ValidationError('Empty data not permitted')
        data = self.validate_data(request.data)
        serializers = serializer_class(data, many=True)
        return Response(serializers.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request, *args, **kwargs):
        serializer_class = self.serializer_class or self.get_serializer_class()
        if not request.user.is_superuser:
            return Response("Unauthorized user", status=status.HTTP_403_FORBIDDEN)
        if not isinstance(request.data, list):
            raise ValidationError('Request body must be a list')
        if request.data == []:
            raise ValidationError('Empty data not permitted')
        ids = self.validate_ids(request.data)
        instances = serializer_class.Meta.model.objects.filter(id__in=ids)
        instances.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)