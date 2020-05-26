import django_filters
from core.models import ClientCreditForm


class ClientCreditFormFilter(django_filters.FilterSet):
    created_time = django_filters.IsoDateTimeFilter(field_name='created_time', lookup_expr='exact')
    modified_time = django_filters.IsoDateTimeFilter(field_name='modified_time', lookup_expr='exact')
    created_time__gt = django_filters.IsoDateTimeFilter(field_name='created_time', lookup_expr='gt')
    created_time__lt = django_filters.IsoDateTimeFilter(field_name='created_time', lookup_expr='lt')
    modified_time__gt = django_filters.IsoDateTimeFilter(field_name='modified_time', lookup_expr='gt')
    modified_time__lt = django_filters.IsoDateTimeFilter(field_name='modified_time', lookup_expr='lt')

    class Meta:
        model = ClientCreditForm
        fields = {
            'lastname': ['exact'],
            'surname': ['exact'],
            'firstname': ['exact'],
            'passport_num': ['exact'],
            'phone_num': ['exact'],
            'birthday': ['exact', 'gt', 'lt'],
            'score': ['exact', 'gt', 'lt']
        }
