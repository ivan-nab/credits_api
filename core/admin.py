from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import Organization
from core.models import CreditOffer, CreditOfferType, ClientCreditForm, CreditRequest
from django.contrib.auth.forms import UserChangeForm

# Register your models here.
# admin.site.register(CreditOffer)
admin.site.register(CreditOfferType)
# admin.site.register(ClientCreditForm)


@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('created_time',)
    list_display = ('created_time', 'sent_time', 'client_credit_form', 'credit_offer')
    list_filter = ('credit_offer__credit_org',)
    search_fields = ['client_credit_form__lastname', 'client_credit_form__surname', 'client_credit_form__firstname']
    raw_id_fields = ('credit_offer', 'client_credit_form')


#Расширяем стандартную пользовательскую админку
class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Organization


class MyUserAdmin(UserAdmin):
    list_display = ('username', 'name', 'email','is_staff')
    form = MyUserChangeForm
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('name', )}), )


admin.site.register(Organization, MyUserAdmin)


@admin.register(ClientCreditForm)
class ClientCreditFormAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'surname', 'lastname', 'phone_num', 'passport_num', 'score', 'partner')
    list_filter = ('partner__name', )
    readonly_fields = ('created_time', 'modified_time', )
    search_fields = ('firstname', 'surname',)
    raw_id_fields = ('partner',)

    # На случай если необходимо выбирать партнеров из combobox
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Returns organizations only from "partners" group
        """
        if db_field.name == "partner":
            kwargs["queryset"] = Organization.objects.filter(groups__name='partners')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(CreditOffer)
class CreditOfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'rotation_start_time', 'rotation_end_time', 'type',
                    'min_score', 'max_score', 'credit_org')
    list_filter = ('credit_org__name', 'type')
    readonly_fields = (
        'created_time',
        'modified_time',
    )
    search_fields = ('name',)
    raw_id_fields = ('credit_org', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Returns organizations only from "banks" group
        """
        if db_field.name == "credit_org":
            kwargs["queryset"] = Organization.objects.filter(groups__name='banks')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
