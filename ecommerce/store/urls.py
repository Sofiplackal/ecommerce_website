from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    


	# extra


    # path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('wishlist_view/', views.wishlist_view, name='wishlist'),  # View wishlist
    

    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
     path('product/<int:product_id>/', views.product_detail, name='product_detail'),
     
]
    


    
    




	
