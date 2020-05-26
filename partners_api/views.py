from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from core.filters import ClientCreditFormFilter
from core.models import ClientCreditForm, CreditOffer, CreditRequest
from partners_api.permissions import (ClientCreditFormAccessPolicy, CreditOfferAccessPolicy, CreditRequestAccessPolicy)
from partners_api.serializers import (AdminClientCreditFormSerializer, ClientCreditFormSerializer,
                                      CreditOfferReadSerializer, CreditRequestSerializer, CreditRequestWriteSerializer)


class CreditOfferViewSet(viewsets.ModelViewSet):
    """
    API endpoint for edit or view banks credit offers
    """
    queryset = CreditOffer.objects.all()
    permission_classes = (CreditOfferAccessPolicy, )
    serializer_class = CreditOfferReadSerializer


class ClientCreditFormViewSet(viewsets.ModelViewSet):
    """
    API endpoint for create, edit or view credit forms
    """
    permission_classes = (ClientCreditFormAccessPolicy, )
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ClientCreditFormFilter
    ordering_fields = [
        'id', 'created_time', 'modified_time', 'lastname', 'surname', 'firstname', 'birthday', 'phone_num',
        'passport_num', 'score'
    ]

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return self.access_policy.scope_queryset(self.request, ClientCreditForm.objects.all())

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            return serializer.save()
        return serializer.save(partner=self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminClientCreditFormSerializer
        return ClientCreditFormSerializer

    @swagger_auto_schema(method='GET', responses={200: CreditOfferReadSerializer})
    @action(methods=['GET'], detail=True, url_path='relevant-offers')
    def relevant_offers(self, request, pk):
        """
        Action for get list relevant credit offers
        """
        client_credit_form = self.get_object()
        if request.method == 'GET':
            # список предложений, подходящих к анкете
            offers_qs = client_credit_form.get_relevant_offers()
            serializer = CreditOfferReadSerializer(offers_qs, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(method='POST',
                         request_body=CreditRequestWriteSerializer,
                         responses={201: CreditRequestSerializer(many=True)})
    @action(methods=['POST'], detail=True, url_path='send-to-banks')
    def send_to_banks(self, request, pk):
        """
        Action for send credit form to credit organizations
        input parameters: list with credit offer id's
        if input parameters is blank credit form will be sent to all 
        credit organizations
        Example: {
                    'credit_offers': [1, 2]
                }
        """
        serializer = CreditRequestWriteSerializer(data=request.data, context={'credit_form_id': pk})
        serializer.is_valid(raise_exception=True)
        instances = serializer.save()
        response_data = CreditRequestSerializer(instances, many=True).data
        return Response(response_data, status=HTTP_201_CREATED)


class CreditRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint for create, edit or view requests for credit
    """
    queryset = CreditRequest.objects.all()
    permission_classes = (CreditRequestAccessPolicy, )
    serializer_class = CreditRequestSerializer
    filter_backends = [DjangoFilterBackend]

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return self.access_policy.scope_queryset(self.request, CreditRequest.objects.all())
