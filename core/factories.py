import factory
from faker import Faker

from django.contrib.auth.models import Group
from core.models import (ClientCreditForm, CreditOffer, CreditRequest, CreditOffer, CreditOfferType, Organization,
                         CreditRequest)

faker = Faker()


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group
        django_get_or_create = ('name', )

    name = "banks"


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization
        django_get_or_create = ('username', )

    username = factory.LazyAttribute(lambda obj: faker.simple_profile()['username'])
    name = factory.LazyAttribute(lambda obj: faker.company())
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    password = faker.password()

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)


class ClientCreditFormFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClientCreditForm

    firstname = factory.LazyAttribute(lambda obj: faker.first_name())
    lastname = factory.LazyAttribute(lambda obj: faker.last_name())
    surname = factory.LazyAttribute(lambda obj: faker.first_name())
    birthday = factory.LazyAttribute(lambda obj: faker.date_between())
    phone_num = factory.LazyAttribute(lambda obj: faker.phone_number())
    passport_num = factory.LazyAttribute(lambda obj: faker.bothify(text='####-######'))
    score = factory.LazyAttribute(lambda obj: faker.random_int(min=1, max=999))
    partner = factory.SubFactory(OrganizationFactory)


class CreditOfferTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CreditOfferType

    name = factory.LazyAttribute(lambda obj: faker.name())


class CreditOfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CreditOffer

    rotation_start_time = factory.LazyAttribute(lambda obj: faker.past_datetime(start_date="-30d", tzinfo=None))
    rotation_end_time = factory.LazyAttribute(lambda obj: faker.past_datetime(start_date="-30d", tzinfo=None))
    name = factory.LazyAttribute(lambda obj: faker.name())
    type = factory.SubFactory(CreditOfferTypeFactory)
    min_score = factory.LazyAttribute(lambda obj: faker.random_int(min=1, max=999))
    max_score = factory.LazyAttribute(lambda obj: faker.random_int(min=1, max=999))
    credit_org = factory.SubFactory(OrganizationFactory)


class CreditRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CreditRequest

    client_credit_form = factory.SubFactory(ClientCreditFormFactory)
    credit_offer = factory.SubFactory(CreditOfferFactory)
    status = "new"