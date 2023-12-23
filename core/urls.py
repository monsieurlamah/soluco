from django.urls import path, include
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
    
    #Add-to-cart
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    
    #Cart view
    path("panier/", views.cart_view, name="core-cart"),
    
    #Delete item from cart
    path("delete-from-cart/", views.delete_from_cart, name="delete-from-cart"),
    
    #Update item from cart
    path("update-cart/", views.update_cart, name="update-cart"),
    
    #checkout
    path('paiement/', views.checkout_view, name="core-checkout"),
    
    #paypal url
    path('paypal/', include("paypal.standard.ipn.urls")),
    
    #payment completed
    path('payment-completed/', views.payment_completed_view, name='core-payment-completed'),
    
    #payment failed
    path('payment-failed/', views.payment_failed_view, name='core-payment-failed'),
    
    #dashboard
    path('dashboard/', views.customer_dashboard, name="core-dashboard"),
    
    #order-detail
    path('dashboard/commande/<int:id>', views.order_detail, name="core-order-detail"),
    
    #make-default-address
    path('make-default-address/', views.make_address_default, name="make-default-address"),
    
    #wishlist
    path('wishlist/', views.wishlistPage, name="core-wishlist"),
    
    #adding wishlist
    path('add-to-wishlist/', views.add_to_wishlist, name="add-to-wishlist"),
    
    #removing wishlist
    path('remove-from-wishlist/', views.remove_wishlist, name="remove-from-wishlist"),
    
    #===============OTHERS PAGES================
    #contact
    path('contact/', views.contact, name="core-contact"),
    path('ajax-contact-form/', views.ajax_contact_form, name="ajax-contact-form"),
    path('a-propos/', views.about_us, name="core-about"),
    path('guide/', views.purchase_guide, name="core-guide"),
    path('politique-de-confidentialite/', views.privacy_policy, name="core-policy"),
    path('conditions-utilisation/', views.terms_of_service, name="core-condition"),
    
]
