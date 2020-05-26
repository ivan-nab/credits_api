from rest_access_policy import AccessPolicy


class CreditRequestAccessPolicy(AccessPolicy):
    statements = [{
        "action": ["list", "retrieve", "set_status"],
        "principal": ["group:banks"],
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
        return qs.filter(credit_offer__credit_org=request.user)
