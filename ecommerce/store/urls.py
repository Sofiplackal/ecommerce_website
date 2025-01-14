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


    
    # path('wishlist_view/', views.wishlist_view, name='wishlist'),  # View wishlist
    

    # path('wishlist/', views.wishlist_view, name='wishlist_view'),
    # path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    # path('wishlist/remove/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    # path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('about/', views.about_view, name='about'),
    
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    #  path('update_wishlist/', views.update_wishlist, name='update_wishlist'),
    # path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    # path('wishlist_view/', views.wishlist_view, name='wishlist'),
    # path('remove-from-wishlist/<int:wishlist_item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
   
    # path('wishlist_page/', views.wishlist_page, name='wishlist_page'),
    # Other URLs for product details or store page
    #  path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
     
     path('wishlist/', views.wishlist_view, name='wishlist'),  # Wishlist page
     path('product/<int:product_id>/', views.product_detail, name='product_detail'),
#    path('product/<int:product_id>/review/', views.submit_review, name='product_review'),



   
]
   



    
    




	
