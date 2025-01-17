from django.urls import path

from apps.notification import views


urlpatterns = [
    path('broadcasted/', views.BroadcastListView.as_view(),
         name='broadcast-notification-list'),
]
