from django.shortcuts import render

# Create your views here.
from .models import User
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import pagination
import rest_framework
from rest_framework import viewsets, filters


class AtomicloopsPagination(pagination.LimitOffsetPagination):
    # default_limit = 10
    pass

class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
     # Explicitly specify which fields the API may be ordered against
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ('first_name', 'last_name', 'createdAt')

    # This will be used as the default ordering
    ordering = ('-createdAt',)
    # pagination_class = rest_framework.pagination.PageNumberPagination
    # page_size = 10
    # pagination_class = AtomicloopsPagination
    # page_size = 10


    # pagination_class = LimitOffsetPagination
    # filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    # search_fields = ('username', 'first_name', 'last_name', 'email')
    # filt

    # @action(detail=False, methods=['get'], url_path='api')
    # def bulk_update(self, request, *args, **kwargs):
    #     return Response("Hello")

    # def list(self, request, *args, **kwargs):
    #     data = User.objects.all()[:10]
    #     data = UserSerializer(data, many=True)
    #     return Response(data.data)