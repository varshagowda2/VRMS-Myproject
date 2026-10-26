from django.contrib import admin
from .models import (
    Customer,
    Vehicle,
    Reservation,
    FleetInspection,
    InsurancePolicy,
    InsuranceAudit,
    Invoice,
    Payment,
)

admin.site.register(Customer)
admin.site.register(Vehicle)
admin.site.register(Reservation)
admin.site.register(FleetInspection)
admin.site.register(InsurancePolicy)
admin.site.register(InsuranceAudit)
admin.site.register(Invoice)
admin.site.register(Payment)