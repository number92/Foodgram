from rest_framework.pagination import PageNumberPagination


class LimitPagination(PageNumberPagination):
    """Стандартный пагинатор с параметром вывода
    количества обьектов на странице по лимиту
    """
    page_size_query_param = 'limit'
