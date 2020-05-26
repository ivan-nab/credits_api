from rest_framework.serializers import ModelSerializer, StringRelatedField, Serializer, ChoiceField
from core.models import CreditRequest, ClientCreditForm, CreditOffer


class StatusSerializer(Serializer):
    STATUS_CHOICES = (('approved', 'Одобрено'), ('denied', 'Отказано'), ('issued', 'Выдано'))
    status = ChoiceField(choices=STATUS_CHOICES)


class CreditOfferSerializer(ModelSerializer):
    type = StringRelatedField()

    class Meta:
        model = CreditOffer
        fields = ['name', 'type']


class ClientCreditFormSerializer(ModelSerializer):
    partner = StringRelatedField()

    class Meta:
        model = ClientCreditForm
        fields = ('lastname', 'surname', 'firstname', 'birthday', 'phone_num', 'passport_num', 'score', 'partner')


class CreditRequestReadSerializer(ModelSerializer):
    client_credit_form = ClientCreditFormSerializer()
    credit_offer = CreditOfferSerializer()

    class Meta:
        model = CreditRequest
        fields = ('id', 'created_time', 'sent_time', 'client_credit_form', 'credit_offer', 'status')