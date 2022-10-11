from django.urls import include, path

from apps.product import views


urlpatterns = [
    path('', views.ProductListView.as_view(),
         name='product-list'),
    path('search/', views.ProductSearchView.as_view(),
         name='product-search'),
    path('<slug:slug>/', views.ProductDetailView.as_view(),
         name='product-detail'),
]

