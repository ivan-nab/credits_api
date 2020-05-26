from rest_framework.serializers import (HyperlinkedModelSerializer, ModelSerializer, PrimaryKeyRelatedField)

from core.models import (ClientCreditForm, CreditOffer, CreditOfferType, CreditRequest, Organization)


class OrganizationSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']


class ClientCreditFormSerializer(ModelSerializer):
    class Meta:
        model = ClientCreditForm
        fields = ('id', 'created_time', 'modified_time', 'lastname', 'surname', 'firstname', 'birthday', 'phone_num',
                  'passport_num', 'score')


class AdminClientCreditFormSerializer(ClientCreditFormSerializer):
    class Meta(ClientCreditFormSerializer.Meta):
        model = ClientCreditForm
        fields = ClientCreditFormSerializer.Meta.fields + ('partner', )


class CreditOfferReadSerializer(ModelSerializer):
    credit_org = OrganizationSerializer(read_only=True)

    class Meta:
        model = CreditOffer
        fields = '__all__'


class CreditOfferTypeSerializer(ModelSerializer):
    class Meta:
        model = CreditOfferType
        fields = ('id', 'name')


class CreditRequestSerializer(ModelSerializer):
    class Meta:
        model = CreditRequest
        fields = '__all__'


class CreditRequestWriteSerializer(ModelSerializer):
    credit_offers = PrimaryKeyRelatedField(many=True, queryset=CreditOffer.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(CreditRequestWriteSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = CreditRequest
        fields = ('client_credit_form', 'credit_offers', 'credit_offer')
        extra_kwargs = {
            "credit_offers": {
                "write_only": True
            },
            "credit_offer": {
                "read_only": True
            },
            "client_credit_form": {
                "read_only": True
            }
        }

    def create(self, validated_data):
        offers = validated_data.pop('credit_offers', CreditOffer.objects.all())
        client_credit_form = ClientCreditForm.objects.get(id=self.context.get('credit_form_id'))
        # Предполагаем, что предложений немного. Если много, то следует делать bulk_create,
        # если очень много, то делать асинхронно через celery
        requests = [
            CreditRequest.objects.create(**validated_data, client_credit_form=client_credit_form, credit_offer=offer)
            for offer in offers
        ]
        return requests
