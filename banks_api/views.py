from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from banks_api.permissions import CreditRequestAccessPolicy
from banks_api.serializers import CreditRequestReadSerializer, StatusSerializer
from banks_api.filters import ClientRequestFormFilter

from core.models import CreditRequest


class CreditRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for view credit requests
    """
    queryset = CreditRequest.objects.all()
    permission_classes = (CreditRequestAccessPolicy, )
    serializer_class = CreditRequestReadSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ClientRequestFormFilter
    ordering_fields = [
        'created_time', 'sent_time', 'client_credit_form__lastname', 'client_credit_form__surname',
        'client_credit_form__firstname', 'client_credit_form__passport_num', 'client_credit_form__phone_num',
        'client_credit_form__birthday', 'client_credit_form__score', 'status'
    ]

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return self.access_policy.scope_queryset(self.request, CreditRequest.objects.all())

    @action(methods=['POST'], detail=True, url_path='set-status')
    def set_status(self, request, pk):
        """
        Action for change request status
        """
        credit_request = self.get_object()
        serializer = StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        credit_request.set_status(serializer.validated_data.pop('status'))
        response_data = CreditRequestReadSerializer(credit_request).data
        return Response(response_data, status=HTTP_200_OK)
