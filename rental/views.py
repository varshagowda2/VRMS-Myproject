from django.shortcuts import render
from django.db.models import Sum
from .models import (
    Vehicle, Customer, Reservation, Invoice, Payment
)


def home(request):
    return render(request, "rental/home.html")


def dashboard(request):
    context = {
        "total_vehicles": Vehicle.objects.count(),
        "available_vehicles": Vehicle.objects.filter(
            status="AVAILABLE"
        ).count(),
        "total_customers": Customer.objects.count(),
        "total_reservations": Reservation.objects.count(),
        "active_reservations": Reservation.objects.filter(
            status="ACTIVE"
        ).count(),
        "total_payments": (
            Payment.objects.aggregate(total=Sum("amount"))["total"]
            or 0
        ),
        "recent_reservations": Reservation.objects.select_related(
            "customer", "vehicle"
        ).order_by("-id")[:5],
        "total_invoices": Invoice.objects.count(),
        "unpaid_invoices": Invoice.objects.filter(
            status__in=["UNPAID", "PARTIAL", "OVERDUE"]
        ).count(),
    }

    return render(request, "rental/dashboard.html", context)


def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(
        request,
        "rental/vehicle_list.html",
        {"vehicles": vehicles},
    )


def customer_list(request):
    customers = Customer.objects.all()
    return render(
        request,
        "rental/customer_list.html",
        {"customers": customers},
    )


def reservation_list(request):
    reservations = Reservation.objects.select_related(
        "customer", "vehicle"
    ).all()

    return render(
        request,
        "rental/reservation_list.html",
        {"reservations": reservations},
    )
def privacy_policy(request):
    return render(request, "rental/privacy_policy.html")
def terms(request):
    return render(request, "rental/terms.html")