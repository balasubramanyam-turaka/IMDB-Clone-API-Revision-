from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchListPagination(PageNumberPagination):
  page_size = 7 #how many elements should be there in single page (Lets say we are having 21 first page will have 10, then next page will have 10 elements)
  page_query_param = 'p' #we rename our query using this like eariler we used access like ?page=2 now ?p=2 it will work..
  page_size_query_param = 'size' 
  max_page_size = 10
  last_page_strings = 'end'
  

class WatchListLOPagination(LimitOffsetPagination):
  default_limit = 5
  max_limit = 10
  limit_query_param = 'limit'
  offset_query_param ='start'


class WatchListCPagination(CursorPagination):
  page_size = 2
  ordering = 'created' 
  cursor_query_param = 'record'  