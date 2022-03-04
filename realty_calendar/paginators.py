from collections import OrderedDict

from django.core.paginator import InvalidPage

from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'psz'
    max_page_size = 9999999

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        if request.query_params.get('no_paging') is not None:
            page_size = int(len(queryset))

        if page_size == 0:
            page_size = 1

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_page_number(self, request, paginator):
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        return page_number

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('pages_count', int(self.page.paginator.count / self.page_size) + 1),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
