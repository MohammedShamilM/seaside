
from .models import WhishlistItem,wishlist
from cartandcheckout.models import cart,CartItem

# def wishlist_count(request):
#     if request.user.is_authenticated:
#         try:
#             # Get a single instance of the user's wishlist
#             wish_list = wishlist.objects.get(user=request.user)
#             count = WhishlistItem.objects.filter(Wishlist=wish_list).count()
#         except wish_list.DoesNotExist:
#             count = 0
#     else:
#         count = 0
#     return {'wishlist_count': count}


