from urllib.parse import urljoin

from django.utils.dateparse import parse_datetime
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
# Create your tests here.
from rest_framework.test import APITestCase

from partners_api.serializers import (AdminClientCreditFormSerializer, ClientCreditFormSerializer,
                                      CreditOfferReadSerializer, CreditRequestSerializer)

from core.factories import (ClientCreditFormFactory, GroupFactory, OrganizationFactory, CreditOfferFactory)


class ClientCreditFormTestCase(APITestCase):

    url = reverse('creditforms-list')

    def setUp(self):
        super(ClientCreditFormTestCase, self).setUp()
        self.partner_user = OrganizationFactory(groups=(GroupFactory(name='partners'), ))
        self.bank_user = OrganizationFactory(groups=(GroupFactory(name='banks'), ))
        self.credit_form = ClientCreditFormFactory(partner=self.partner_user)

    def test_get_creditforms(self):
        self.client.force_authenticate(user=self.partner_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_creditforms_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_creditforms_for_banks(self):
        self.client.force_authenticate(user=self.bank_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_creditform(self):
        self.client.force_authenticate(user=self.partner_user)
        new_form = ClientCreditFormFactory(partner=self.partner_user)
        data = ClientCreditFormSerializer(new_form).data
        response = self.client.post(self.url, data)
        data.pop('id')
        data.pop('created_time')
        data.pop('modified_time')
        response.data.pop('modified_time')
        response.data.pop('created_time')
        response.data.pop('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data, response.data)

    def test_create_creditform_by_bank(self):
        self.client.force_authenticate(user=self.bank_user)
        new_form = ClientCreditFormFactory(partner=self.partner_user)
        data = ClientCreditFormSerializer(new_form).data
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_creditform_by_admin(self):
        admin_user = OrganizationFactory(is_staff=True)
        self.client.force_authenticate(user=admin_user)
        new_form = ClientCreditFormFactory(partner=self.partner_user)
        data = AdminClientCreditFormSerializer(new_form).data
        response = self.client.post(self.url, data)
        data.pop('id')
        data.pop('created_time')
        data.pop('modified_time')
        response.data.pop('modified_time', None)
        response.data.pop('created_time')
        response.data.pop('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data, response.data)

    def test_update_creditform_by_admin(self):
        admin_user = OrganizationFactory(is_staff=True)
        self.client.force_authenticate(user=admin_user)
        new_form = ClientCreditFormFactory(partner=self.partner_user)
        data = AdminClientCreditFormSerializer(new_form).data
        expected_field = "UpdatedField"
        data['lastname'] = expected_field
        form_url = urljoin(self.url, f'{new_form.id}/')
        response = self.client.put(form_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_field, response.data['lastname'])

    def test_update_creditform_by_partner(self):
        self.client.force_authenticate(user=self.partner_user)
        new_form = ClientCreditFormFactory(partner=self.partner_user)
        data = AdminClientCreditFormSerializer(new_form).data
        expected_field = "UpdatedField"
        data['lastname'] = expected_field
        form_url = urljoin(self.url, f'{new_form.id}/')
        response = self.client.put(form_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_creditform_by_bank(self):
        self.client.force_authenticate(user=self.bank_user)
        new_form = ClientCreditFormFactory(partner=self.partner_user)
        data = AdminClientCreditFormSerializer(new_form).data
        expected_field = "UpdatedField"
        data['lastname'] = expected_field
        form_url = urljoin(self.url, f'{new_form.id}/')
        response = self.client.put(form_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_relevant_offers(self):
        self.client.force_authenticate(user=self.partner_user)
        bank1 = OrganizationFactory(groups=(GroupFactory(name="banks"), ))
        bank2 = OrganizationFactory(groups=(GroupFactory(name="banks"), ))
        relevant_offer1 = CreditOfferFactory(rotation_start_time=parse_datetime('2000-01-01T00:00:00'),
                                             rotation_end_time=parse_datetime('2023-01-01T00:00:00'),
                                             min_score=200,
                                             max_score=400,
                                             credit_org=bank1)

        not_relevant_offer1 = CreditOfferFactory(rotation_start_time=parse_datetime('2000-01-01T00:00:00'),
                                                 rotation_end_time=parse_datetime('2023-01-01T00:00:00'),
                                                 min_score=800,
                                                 max_score=999,
                                                 credit_org=bank2)
        credit_form = ClientCreditFormFactory(score=300, partner=self.partner_user)
        offers = credit_form.get_relevant_offers()
        self.assertEqual(len(offers), 1)
        self.assertEqual(relevant_offer1, offers[0])
        form_action_url = reverse('creditforms-relevant-offers', args=[credit_form.id])
        expected_data = CreditOfferReadSerializer(offers, many=True).data
        response = self.client.get(form_action_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_send_to_banks(self):
        self.client.force_authenticate(user=self.partner_user)
        bank1 = OrganizationFactory(groups=(GroupFactory(name="banks"), ))
        bank2 = OrganizationFactory(groups=(GroupFactory(name="banks"), ))
        offers = [
            CreditOfferFactory(rotation_start_time=parse_datetime('2000-01-01T00:00:00'),
                               rotation_end_time=parse_datetime('2023-01-01T00:00:00'),
                               min_score=200,
                               max_score=400,
                               credit_org=bank1),
            CreditOfferFactory(rotation_start_time=parse_datetime('2000-01-01T00:00:00'),
                               rotation_end_time=parse_datetime('2023-01-01T00:00:00'),
                               min_score=300,
                               max_score=999,
                               credit_org=bank2)
        ]
        credit_form = ClientCreditFormFactory(score=300, partner=self.partner_user)
        form_action_url = reverse('creditforms-send-to-banks', args=[credit_form.id])
        response = self.client.post(form_action_url, data={"credit_offers": [offers[0].id]})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['credit_offer'], offers[0].id)

    def test_send_to_all_banks(self):
        self.client.force_authenticate(user=self.partner_user)
        bank1 = OrganizationFactory(groups=(GroupFactory(name="banks"), ))
        bank2 = OrganizationFactory(groups=(GroupFactory(name="banks"), ))
        offers = [
            CreditOfferFactory(rotation_start_time=parse_datetime('2000-01-01T00:00:00'),
                               rotation_end_time=parse_datetime('2023-01-01T00:00:00'),
                               min_score=200,
                               max_score=400,
                               credit_org=bank1),
            CreditOfferFactory(rotation_start_time=parse_datetime('2000-01-01T00:00:00'),
                               rotation_end_time=parse_datetime('2023-01-01T00:00:00'),
                               min_score=300,
                               max_score=999,
                               credit_org=bank2)
        ]
        credit_form = ClientCreditFormFactory(score=300, partner=self.partner_user)
        form_action_url = reverse('creditforms-send-to-banks', args=[credit_form.id])
        response = self.client.post(form_action_url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['credit_offer'], offers[0].id)
        self.assertEqual(response.data[0]['client_credit_form'], credit_form.id)
        self.assertEqual(response.data[1]['credit_offer'], offers[1].id)
        self.assertEqual(response.data[1]['client_credit_form'], credit_form.id)