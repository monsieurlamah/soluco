from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name="core-index"),
    
    #Product
    path('produits/', views.product_list_view, name="core-product-list"),
    path('produit/<pid>/', views.product_detail_view, name="core-product-detail"),
    
    #Category
    path('categories/', views.category_list_view, name="core-category-list"),
    path('categorie/<cid>/', views.category_product_list, name="core-category-product-list"),
    
    #vendor
    path('fournisseurs/', views.vendor_list_view, name="core-vendor-list"),
    path('fournisseur/<vid>/', views.vendor_detail_view, name="core-vendor-detail"),
    
    #Tags
    path('products/tag/<slug:tag_slug>/', views.tag_list, name="core-tags"),
    
    #Add review
    path('ajax-add-review/<pid>/', views.ajax_add_review, name="core-ajax-add-review"),
    
    #search
    path('recherche/', views.sarch_view, name="app-search"),
    
    #filter
    path('filter-product/', views.filter_product, name="filter-product"),
]
