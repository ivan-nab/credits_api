from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from . import choices


class Organization(AbstractUser):
    name = models.CharField(verbose_name='Название организации', max_length=100)

    def __str__(self):
        return self.name


class CreditOfferType(models.Model):
    name = models.CharField(verbose_name='Название типа предложения', max_length=20)

    def __str__(self):
        return self.name


class CreditOffer(models.Model):
    created_time = models.DateTimeField(verbose_name='Дата и время создания', auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name='Дата и время изменения', auto_now=True)
    rotation_start_time = models.DateTimeField(verbose_name='Дата и время начала ротации')
    rotation_end_time = models.DateTimeField(verbose_name='Дата и время окончания ротации')
    name = models.CharField(verbose_name='Название предложения', max_length=200)
    type = models.ForeignKey(verbose_name='Тип предложения', to=CreditOfferType, on_delete=models.CASCADE)
    min_score = models.PositiveSmallIntegerField(verbose_name='Минимальный скоринговый балл',
                                                 validators=[MinValueValidator(1),
                                                             MaxValueValidator(1000)])
    max_score = models.PositiveSmallIntegerField(verbose_name='Максимальный скоринговый балл',
                                                 validators=[MinValueValidator(1),
                                                             MaxValueValidator(1000)])
    credit_org = models.ForeignKey(verbose_name='Кредитная организация', to=Organization, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {} - {}".format(self.type, self.name, self.credit_org.name)


class ClientCreditForm(models.Model):
    created_time = models.DateTimeField(verbose_name='Дата и время создания', auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name='Дата и время изменения', auto_now=True)
    lastname = models.CharField(verbose_name='Фамилия клиента', max_length=100)
    surname = models.CharField(verbose_name='Отчество клиента', max_length=100)
    firstname = models.CharField(verbose_name='Имя клиента', max_length=100)
    birthday = models.DateField(verbose_name='Дата рождения клиента')
    phone_num = models.CharField(verbose_name='Номер телефона', max_length=20)
    passport_num = models.CharField(verbose_name='Номер паспорта', max_length=20)
    score = models.IntegerField(verbose_name='Cкоринговый балл клиента',
                                validators=[MinValueValidator(1), MaxValueValidator(1000)])
    partner = models.ForeignKey(verbose_name='Партнер', to=Organization, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {} {}".format(self.firstname, self.surname, self.lastname)

    def get_relevant_offers(self):
        """
        Method returns relevant credit offer for current client form
        """
        return CreditOffer.objects.filter(min_score__lte=self.score,
                                          max_score__gte=self.score,
                                          rotation_start_time__lte=self.created_time,
                                          rotation_end_time__gte=self.created_time).all()


class CreditRequest(models.Model):
    created_time = models.DateTimeField(verbose_name='Дата и время создания', auto_now_add=True)
    sent_time = models.DateTimeField(verbose_name='Дата и время отправки', auto_now_add=True)
    client_credit_form = models.ForeignKey(verbose_name='Анкета клиента', to=ClientCreditForm, on_delete=models.CASCADE)
    credit_offer = models.ForeignKey(verbose_name='Кредитное предложение', to=CreditOffer, on_delete=models.CASCADE)
    status = models.CharField(verbose_name='Статус', max_length=20, choices=choices.STATUS_CHOICES, default='new')

    def set_status(self, status):
        self.status = status
        self.save()
