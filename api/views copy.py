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
from .viewsets import AtomicViewSet
from sys import getsizeof
import time

from rest_framework import status
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class AtomicloopsPagination(pagination.LimitOffsetPagination):
    # default_limit = 10
    pass

class UserView(ModelViewSet):
    # queryset = User.objects.all()

    serializer_class = UserSerializer
     # Explicitly specify which fields the API may be ordered against
    # filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # ordering_fields = ('first_name', 'last_name', 'email')

    # This will be used as the default ordering
    # ordering = ('-createdAt',)
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

    def get_queryset(self):
        print('QUERY CALLED')
        return User.objects.all()
        # print(self.request.query_params.__dict__)
        query_params = dict(zip(self.request.GET.keys(), self.request.GET.values()))
        # print(query_params)
        # print(len(query_params))
        print(cache.keys('*'))
        # cache.clear()


        if len(query_params) > 1:
            print('Not do caching')
            return User.objects.all()
        else:
            if 'page' in query_params:
                page = int(query_params['page'])
            else:
                page = 1
            print(page)

            if f"users_{page}" in cache:
                print('cache')
                queryset = cache.get(f"users_{page}")
                return queryset
            else:
                start, end = 10 * (page - 1), 10 * page
                print(start, end)
                queryset = User.objects.all()[start:end]
                print('Setting in parallel', page)
                cache.set(f"users_{page}", queryset, CACHE_TTL)
                return queryset
        # if len(query_params) <=1 and "page" in query_params:  
        #     page = 1
        # else:
        #     page = int(query_params.get("page", 1))
        
        # if f'users_{page}' in cache:
        #     pass
        # else:
        #     User.objects.all().delete()
        
        # # else:
            
        #     queryset = User.objects.all()

        # print()
        # print(cache)
        # if 'users' in cache:
        #     print("cache")
        #     # start = time.time()
        #     queryset = cache.get('users')
        #     # end = time.time()
        #     # print("Load from cache",end - start)
        # else:
        #     print("not cache")
        #     # start = time.time()
        #     queryset = User.objects.all()
        #     data = [query.__dict__ for query in queryset]
        #     # end = time.time()
        #     # print("Load from db",end - start)
        #     # store data in cache 
        #     # start = time.time()
        #     cache.set("users", data, timeout=CACHE_TTL)
            # end = time.time()
            # print("Store in cache",end - start)
        # print(getsizeof(queryset))
        queryset = User.objects.all()
        return queryset