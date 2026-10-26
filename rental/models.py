from django.db import models
from django.conf import settings


class Customer(models.Model):
    full_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    driving_license_number = models.CharField(
        max_length=40, unique=True
    )
    address = models.TextField()

    def __str__(self):
        return self.full_name


class Vehicle(models.Model):
    CATEGORY_CHOICES = [
        ("HATCHBACK", "Hatchback"),
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("LUXURY", "Luxury"),
    ]

    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("RENTED", "Rented"),
        ("MAINTENANCE", "Under Maintenance"),
        ("INACTIVE", "Inactive"),
    ]

    registration_number = models.CharField(
        max_length=20, unique=True
    )
    brand = models.CharField(max_length=60)
    model_name = models.CharField(max_length=60)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES
    )
    manufacturing_year = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=30)
    transmission = models.CharField(max_length=30)
    price_per_day = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="AVAILABLE",
    )

    def __str__(self):
        return f"{self.brand} {self.model_name}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("ACTIVE", "Active"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.PROTECT
    )
    pickup_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    def __str__(self):
        return f"Reservation #{self.pk}"

class FleetInspection(models.Model):
    CONDITION_CHOICES = [
        ("GOOD", "Good"),
        ("FAIR", "Fair"),
        ("POOR", "Poor"),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="inspections",
    )
    inspection_date = models.DateField()
    inspector_name = models.CharField(max_length=100)
    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES,
    )
    remarks = models.TextField(blank=True)
    next_inspection_date = models.DateField(
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.vehicle} - {self.inspection_date}"


class InsurancePolicy(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE
    )
    provider = models.CharField(max_length=120)
    policy_number = models.CharField(
        max_length=60, unique=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    coverage_amount = models.DecimalField(
        max_digits=12, decimal_places=2
    )
    premium_amount = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    def __str__(self):
        return self.policy_number


class InsuranceAudit(models.Model):
    policy = models.ForeignKey(
        InsurancePolicy, on_delete=models.CASCADE
    )
    audit_date = models.DateField()
    auditor_name = models.CharField(max_length=100)
    findings = models.TextField()
    action_required = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Audit #{self.pk}"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("UNPAID", "Unpaid"),
        ("PARTIAL", "Partially Paid"),
        ("PAID", "Paid"),
        ("OVERDUE", "Overdue"),
    ]

    reservation = models.ForeignKey(
        Reservation, on_delete=models.PROTECT
    )
    invoice_number = models.CharField(
        max_length=30, unique=True
    )
    issue_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="UNPAID",
    )

    def __str__(self):
        return self.invoice_number


class Payment(models.Model):
    METHOD_CHOICES = [
        ("CASH", "Cash"),
        ("UPI", "UPI"),
        ("CARD", "Card"),
        ("BANK", "Bank Transfer"),
    ]

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        related_name="payments",
    )
    payment_date = models.DateField()
    amount = models.DecimalField(
        max_digits=12, decimal_places=2
    )
    method = models.CharField(
        max_length=10, choices=METHOD_CHOICES
    )
    transaction_reference = models.CharField(
        max_length=100, blank=True
    )

    def __str__(self):
        return f"Payment #{self.pk}"