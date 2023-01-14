from django.shortcuts import render

# Create your views here.
from .models import User
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework import pagination
import rest_framework
from rest_framework import viewsets, filters
from .viewsets import AtomicViewSet
from sys import getsizeof
import time
from collections import OrderedDict
from rest_framework import status
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    # filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ("id",'first_name', 'last_name', 'email')
    search_fields = ('email',)
    filterset_fields = ['first_name', 'last_name']
    pagination_class = pagination.PageNumberPagination


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
   
    @action(detail=False, methods=['get'], url_path='bulk-update')
    def bulk_update(self, request, *args, **kwargs):
        data = self.queryset[:10]
        # data = self.filter_queryset(data)
        context = super().get_serializer_context()
        context.update({"request": self.request})
        data = self.serializer_class(data, many=True, context=context)
        return Response(data.data)

    # def list(self, request, *args, **kwargs):
    #     data = User.objects.all()[:10]
    #     data = UserSerializer(data, many=True)
    #     return Response(data.data)


    
  
