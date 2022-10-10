from django.urls import include, path

from apps.product import views


urlpatterns = [
    path('products/', views.ProductListView.as_view(),
         name='product-list'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(),
         name='product-detail'),
    path('products/search/', views.ProductSearchView.as_view(),
         name='product-search'),
]

