from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response
from collections import OrderedDict, namedtuple

class AtomicPageNumberPagination(PageNumberPagination):
    page_size = 10  
    page_query_param = "p"
    page_size_query_param = "limit"

    def get_paginated_response(self, data):
        print(self.page.paginator.count)
        print(self.page_size_query_param)
        print(self.page_size)
        print(self.get_page_size(self.request))
        return Response(OrderedDict([
            ('total', self.page.paginator.count//self.get_page_size(self.request)),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))



# class PageNumberPagination(BasePagination):
  
#     # The default page size.
#     # Defaults to `None`, meaning pagination is disabled.
#     page_size = api_settings.PAGE_SIZE


#     # Client can control the page using this query parameter.
#     page_query_param = 'page'

#     # Client can control the page size using this query parameter.
#     # Default is 'None'. Set to eg 'page_size' to enable usage.
#     page_size_query_param = None

#     # Set to an integer to limit the maximum page size the client may request.
#     # Only relevant if 'page_size_query_param' has also been set.
#     max_page_size = None




  