from urllib.parse import urljoin

from django.utils.dateparse import parse_datetime
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from banks_api.serializers import CreditRequestReadSerializer
from core.factories import (ClientCreditFormFactory, GroupFactory, OrganizationFactory, CreditOfferFactory,
                            CreditRequestFactory)


class CreditRequestTestCase(APITestCase):

    url = reverse('requests-list')

    def setUp(self):
        super(CreditRequestTestCase, self).setUp()
        self.partner_user = OrganizationFactory(groups=(GroupFactory(name='partners'), ))
        self.bank_user = OrganizationFactory(groups=(GroupFactory(name='banks'), ))
        self.credit_form = ClientCreditFormFactory(partner=self.partner_user)
        self.credit_request = CreditRequestFactory(client_credit_form=self.credit_form,
                                                   credit_offer=CreditOfferFactory(credit_org=self.bank_user))

    def test_get_creditrequests(self):
        self.client.force_authenticate(user=self.bank_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_creditforms_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_creditforms_for_partners(self):
        self.client.force_authenticate(user=self.partner_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_current_bank_requests(self):
        self.client.force_authenticate(user=self.bank_user)
        other_bank = OrganizationFactory(groups=(GroupFactory(name='banks'), ))
        other_credit_request = CreditRequestFactory(client_credit_form=self.credit_form,
                                                    credit_offer=CreditOfferFactory(credit_org=other_bank))
        data = CreditRequestReadSerializer([self.credit_request], many=True).data
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, response.data['results'])

    def test_set_request_status(self):
        self.client.force_authenticate(user=self.bank_user)
        request_url = reverse('requests-set-status', args=[self.credit_request.id])
        response = self.client.post(request_url, data={"status": "approved"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(request_url, data={"status": "new"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(request_url, data={"status": "oiehdwo"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)