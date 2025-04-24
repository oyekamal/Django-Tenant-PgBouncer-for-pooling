from django_tenants.middleware import TenantMainMiddleware

class TenantMiddleware(TenantMainMiddleware):
    def get_tenant(self, domain_model, hostname):
        tenant = super().get_tenant(domain_model, hostname)
        return tenant