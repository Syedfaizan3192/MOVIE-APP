from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchListpage(PageNumberPagination):
    page_size = 1
    # Customize your param name
    page_query_param = "p"
    # Customize your param for user size/100
    page_size_query_param = "size"
    # give max size to user if the size is customize
    max_page_size = 3
    # Get last page bt given string custom your string "last" to any
    last_page_strings = 'end'
    # p/end


class WatchListLOpage(LimitOffsetPagination):
    default_limit = 2
    max_limit = 3
    # Custom Limit query
    limit_query_param = "end"
    # Custom Offset query name
    offset_query_param = "start"


# 	It gives results on the basis of the cursor.
class WatchListCpage(CursorPagination):
    page_size = 3
    # it will by default "-created" 15,14,13,12,11,10
    # Now customizing by converting "-created" to "created:
    ordering = "created"
    # change name cursor to record in link
    cursor_query_param = "record"
