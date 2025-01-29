from django.urls import path

from apps.order import views


urlpatterns = [
    path("checkout/", views.OrderCheckoutView.as_view(), name="order-checkout"),
    path("", views.OrderListView.as_view(), name="order-list"),
]
