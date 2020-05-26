from rest_access_policy import AccessPolicy


class ClientCreditFormAccessPolicy(AccessPolicy):
    statements = [{
        "action": ["create", "list", "retrieve"],
        "principal": ["group:partners"],
        "effect": "allow"
    }, {
        "action": ["relevant_offers", "send_to_banks"],
        "principal": ["group:partners"],
        "effect": "allow"
    }, {
        "action": ["*"],
        "principal": ["*"],
        "effect": "allow",
        "condition": "is_staff"
    }]

    def is_staff(self, request, view, action):
        return request.user.is_staff

    @classmethod
    def scope_queryset(cls, request, qs):
        if request.user.is_staff:
            return qs
        return qs.filter(partner=request.user)


class CreditRequestAccessPolicy(AccessPolicy):
    statements = [{
        "action": ["list", "retrieve"],
        "principal": ["group:partners"],
        "effect": "allow"
    }, {
        "action": ["*"],
        "principal": ["*"],
        "effect": "allow",
        "condition": "is_staff"
    }]

    def is_staff(self, request, view, action):
        return request.user.is_staff

    @classmethod
    def scope_queryset(cls, request, qs):
        if request.user.is_staff:
            return qs
        return qs.filter(client_credit_form__partner=request.user)


class CreditOfferAccessPolicy(AccessPolicy):
    statements = [{
        "action": ["list", "retrieve"],
        "principal": ["group:partners"],
        "effect": "allow"
    }, {
        "action": ["*"],
        "principal": ["*"],
        "effect": "allow",
        "condition": "is_staff"
    }]

    def is_staff(self, request, view, action):
        return request.user.is_staff
