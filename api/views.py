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


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class CustomPagination(pagination.PageNumberPagination):
    pass
    # def paginate_queryset(self, queryset, request, view=None):
    #     paginator = super().django_paginator_class(queryset, 10)
    #     page_number = super().get_page_number(request, paginator)
    #     model_name = request.path.replace('/', '')
    #     key = "%s_%s" % (model_name, page_number)
    #     print(page_number, model_name)
    #     # cache.clear()
    #     if key in cache:
    #         print("cache")
    #         response = cache.get(key)
    #     else:
    #         print("not cache")
    #         print("aksjdfasdjfkasjk",request)
    #         response = super().paginate_queryset(queryset, request)
    #         print(response)
    #         cache.set(key, response, timeout=CACHE_TTL)
    #         # try:
    #         #     self.page = paginator.page(page_number)
    #         # except Exception as exc:
    #         #     msg = self.invalid_page_message.format(
    #         #     page_number=page_number, message=str(exc)
    #         #     )
    #         #     raise "JAKSHk"
    #     self.page = response
    #     self.request = request
    #     return response


        
    # def get_paginated_response(self, data):
    #     # print("asdjf",self.__dir__())
    #     page = self.page.number
    #     model_name = self.request.path.replace('/', '')
    #     key = "%s_%s" % (model_name, page)
    #     if key in cache:
    #         print("cache")
    #         response = cache.get(key)
    #         # print("Load from cache",end - start)
    #     else:
    #         print("not cache")
    #         response = OrderedDict([
    #         ('count', self.page.paginator.count),
    #         ('next', self.get_next_link()),
    #         ('previous', self.get_previous_link()),
    #         ('results', data)
    #         ])
    #         cache.set(key, response, timeout=CACHE_TTL)
    #     return Response(response)
        
        
    ###
        # response = OrderedDict([
        #     ('count', self.page.paginator.count),
        #     ('next', self.get_next_link()),
        #     ('previous', self.get_previous_link()),
        #     ('results', data)
        #     ])
        # return Response(response)
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

    # pagination_class = rest_framework.pagination.PageNumberPagination
    # pagination_class = CustomPagination

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
       
        return User.objects.all()
        # if len(query_params) <=1 and "page" in query_params:  
       
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
    #     return queryset

    
    def list(self, request, *args, **kwargs):
      
        page_number = request.GET.get('page', 1)
        model = self.get_serializer().Meta.model._meta
        key = "%s_%s" % (model, page_number)
        # Use cache
        # cache.clear()
        if (len(request.GET) == 0) or (len(request.GET)==1 and "page" in request.GET):
            if key in cache:
                # print("Cache hit")
                queryset = cache.get(key)
                return Response(queryset)
            else:
                # print("Cache Not hit")
                
                queryset = self.filter_queryset(self.get_queryset())
                page = self.paginate_queryset(queryset)
          
                serializer = self.get_serializer(page, many=True)
                response = self.get_paginated_response(serializer.data).data
              
                # print(response)
                cache.set(key, response, CACHE_TTL)
                return Response(response)
        else:
            # Do not use cache
            # print("Cache Not hit")
            queryset = self.filter_queryset(self.get_queryset())
        
            page = self.paginate_queryset(queryset)
            # print(page)
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data).data
            return Response(response)

        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)