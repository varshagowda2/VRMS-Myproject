from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("vehicles/", views.vehicle_list, name="vehicle_list"),
    path("customers/", views.customer_list, name="customer_list"),
    path("reservations/", views.reservation_list, name="reservation_list"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms/", views.terms, name="terms"),
]