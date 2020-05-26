import django_filters
from core.models import CreditRequest


class ClientRequestFormFilter(django_filters.FilterSet):
    created_time = django_filters.IsoDateTimeFilter(field_name='created_time', lookup_expr='exact')
    modified_time = django_filters.IsoDateTimeFilter(field_name='modified_time', lookup_expr='exact')
    created_time__gt = django_filters.IsoDateTimeFilter(field_name='created_time', lookup_expr='gt')
    created_time__lt = django_filters.IsoDateTimeFilter(field_name='created_time', lookup_expr='lt')
    modified_time__gt = django_filters.IsoDateTimeFilter(field_name='modified_time', lookup_expr='gt')
    modified_time__lt = django_filters.IsoDateTimeFilter(field_name='modified_time', lookup_expr='lt')

    class Meta:
        model = CreditRequest
        fields = {
            'client_credit_form__lastname': ['exact'],
            'client_credit_form__surname': ['exact'],
            'client_credit_form__firstname': ['exact'],
            'client_credit_form__passport_num': ['exact'],
            'client_credit_form__phone_num': ['exact'],
            'client_credit_form__birthday': ['exact', 'gt', 'lt'],
            'client_credit_form__score': ['exact', 'gt', 'lt'],
            'credit_offer__name': ['exact'],
            'credit_offer__type': ['exact'],
            'status': ['exact']
        }
