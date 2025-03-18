from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('categories/', views.CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),
    path('products/', views.ProductListCreate.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroy.as_view(), name='product-detail'),
    path('inventory/<int:product_id>/', views.InventoryRetrieve.as_view(), name='inventory-detail'),
    path('inventory/<int:product_id>/update-stock/', views.InventoryUpdate.as_view(), name='inventory-update'),
]
